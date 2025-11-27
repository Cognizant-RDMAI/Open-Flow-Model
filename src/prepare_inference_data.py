import pandas as pd
import numpy as np
from keras.utils import timeseries_dataset_from_array
import pickle
import os

def load_pickle(path):
    """Load a pickle file from the specified path."""
    with open(path, 'rb') as f:
        return pickle.load(f)

def prepare_data_for_inference(timeseries_df, attributes_df, model_feed_path, sequence_length=30):
    """
    Prepares new timeseries and attribute data for model inference using a saved preprocessor.

    Args:
        timeseries_df (pd.DataFrame): DataFrame containing the new timeseries data.
        attributes_df (pd.DataFrame): DataFrame containing the new attribute data.
        model_feed_path (str): Path to the saved model_feed.pkl file containing preprocessors.
        sequence_length (int): The sequence length used during model training.

    Returns:
        tuple: A tuple containing the processed timeseries data, attribute data, and registry.
    """
    # --- 1. Load Preprocessors and Feature Info ---
    print("Loading preprocessors and feature information...")
    model_feed = load_pickle(model_feed_path)
    X_preprocessor = model_feed['X_preprocessor']
    X_static_preprocessor = model_feed['X_static_preprocessor']
    X_vars_names = model_feed['X_cols_names']
    X_static_vars_names = model_feed['X_static_cols_names']
    
    # --- 2. Window the Timeseries Data ---
    print("Windowing timeseries data...")
    all_sequences = []
    all_targets = []
    registry_list = []

    for catchment_id, group in timeseries_df.groupby('catchmentID'):
        if len(group) < sequence_length:
            print(f"Skipping catchment {catchment_id} due to insufficient data for windowing.")
            continue

        # Ensure columns are in the correct order
        group_features = group[X_vars_names]
        
        dataset = timeseries_dataset_from_array(
            group_features.values,
            targets=group[model_feed.get('label_field_feed', 'discharge_spec')].values[sequence_length-1:],
            sequence_length=sequence_length,
            batch_size=1
        )

        sequences, targets = zip(*[(s, t) for s, t in dataset])
        
        all_sequences.extend(sequences)
        all_targets.extend(targets)
        
        # Create registry for this catchment
        timestamps = [
            (group['date'].iloc[i], group['date'].iloc[i + sequence_length - 1])
            for i in range(len(group) - sequence_length + 1)
        ]
        registry_df = pd.DataFrame(timestamps, columns=['start_date', 'end_date'])
        registry_df['catchmentID'] = catchment_id
        registry_list.append(registry_df)

    if not all_sequences:
        raise ValueError("No valid sequences could be created from the provided timeseries data.")

    X_inference = np.vstack(all_sequences)
    y_inference = np.concatenate(all_targets)
    inference_registry = pd.concat(registry_list, ignore_index=True)

    # --- 3. Scale the Timeseries Data ---
    print("Scaling timeseries data...")
    n_samples, n_timesteps, n_features = X_inference.shape
    X_inference_2d = X_inference.reshape(-1, n_features)
    X_inference_scaled_2d = X_preprocessor.transform(X_inference_2d)
    X_inference_scaled = X_inference_scaled_2d.reshape(n_samples, n_timesteps, n_features)

    # --- 4. Prepare and Scale the Attribute Data ---
    print("Preparing and scaling attribute data...")
    # Merge attributes with the registry
    inference_attributes = inference_registry.merge(
        attributes_df,
        left_on='catchmentID',
        right_index=True,
        how='left'
    ).set_index('catchmentID')
    
    # Ensure columns are in the correct order
    inference_attributes = inference_attributes[X_static_vars_names]
    
    X_inference_static_scaled = X_static_preprocessor.transform(inference_attributes)
    X_inference_static_scaled_df = pd.DataFrame(X_inference_static_scaled, columns=X_static_vars_names)

    print("Data preparation complete.")
    return X_inference_scaled, X_inference_static_scaled_df, y_inference, inference_registry

if __name__ == '__main__':
    # This is an example of how to use the function.
    # You would need to have your data loaded and the model_feed.pkl file available.
    
    # --- Configuration ---
    SILVER_DIR = '../datasets/camels-gb-aggregated/silver'
    MODEL_FEED_PATH = os.path.join(SILVER_DIR, 'model_feed-w30-discharge_spec-1985-cs_Y-train_size_7.pkl')
    
    # --- Load Data ---
    # This assumes you have the aggregated data files available
    try:
        timeseries_df = pd.read_csv('../datasets/camels-gb-aggregated/timeseries_postFEa.csv', parse_dates=['date'])
        attributes_df = pd.read_csv('../datasets/camels-gb-aggregated/attributes/fundamental_postFEa.csv', index_col='catchmentID')
        
        # --- Prepare Data ---
        X_inf, X_static_inf, y_inf, registry_inf = prepare_data_for_inference(
            timeseries_df,
            attributes_df,
            MODEL_FEED_PATH
        )
        
        print("\n--- Output Shapes ---")
        print(f"Inference Timeseries Shape: {X_inf.shape}")
        print(f"Inference Attributes Shape: {X_static_inf.shape}")
        print(f"Inference Labels Shape: {y_inf.shape}")
        print(f"Inference Registry Shape: {registry_inf.shape}")

    except FileNotFoundError as e:
        print(f"Could not run example: {e}")
        print("Please ensure the aggregated data files and the model_feed.pkl file are in their expected locations.")
