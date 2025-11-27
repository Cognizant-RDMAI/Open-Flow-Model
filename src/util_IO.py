# _________
# Libraries
import pickle
import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv, find_dotenv
import contextily as cx

# __________
# Parameters

# Get the main directory
def get_use_case_main_dir():
    directory = os.path.abspath(os.getcwd())
    while os.path.basename(directory) != 'Open-Flow-Model':
        directory = os.path.dirname(directory)
    return directory

# Function to load pickle file with parameters
def load_pickle_from_main_project_dir(
    pickle_file
):
    
    # Main directory
    camels_gb_use_case_dir = get_use_case_main_dir()

    # Read file
    with open(
        os.path.join(
            camels_gb_use_case_dir,
            pickle_file
        ),
        'rb'
    ) as f:
        pickle_file_content = pickle.load(f)

    return pickle_file_content, camels_gb_use_case_dir


# Directories EDA structure
def EDA_dirs_structure():

    # Main directory
    camels_gb_use_case_dir = get_use_case_main_dir()
    
    # Main EDA directory
    camels_gb_eda_dir = os.path.join(
        camels_gb_use_case_dir,
        "resources",
        "EDA"
    )

    # EDA for attributes
    camels_gb_eda_attributes_dir = os.path.join(
        camels_gb_eda_dir,
        "attributes"
    )

    # EDA for time series
    camels_gb_eda_timeseries_dir = os.path.join(
        camels_gb_eda_dir,
        "timeseries"
    )
    
    return camels_gb_eda_dir, camels_gb_eda_attributes_dir, camels_gb_eda_timeseries_dir


# ________
# Datasets

# Attributes
def load_attributes_df(
    dir,
    file,
    index,
    select_columns=None
):

    # Path composition
    path = os.path.join(
        dir,
        file
    )

    # Read the file into a DataFrame
    df = pd.read_csv(
        path,
        dtype={index: 'str'},
        index_col=index
    )

    # Columns selection
    if select_columns==None:
        return df
    else:
        return df[select_columns]

# Timeseries
def load_timeseries_df(
    dir,
    file,
    date_field,
    select_columns=None
):

    # Path composition
    path = os.path.join(
        dir,
        file
    )

    # Read the file into a DataFrame
    df = pd.read_csv(
        path,
        dtype={"catchmentID": 'str'},
        parse_dates=[date_field]
    )

    # Assure group (if present) is string with 2 digits
    if f"{date_field}_group" in df.columns:
        df[f"{date_field}_group"] = (
            df[f"{date_field}_group"]
                .astype(str)
                .str
                .zfill(2)
        )

    # Convert from Timestamp to datetime.date
    df[date_field] = df[date_field].dt.date

    # REDUNDANT STEP, BUT PRECAUTIONARY
    df.sort_values(
        by=[
            "catchmentID",
            date_field
        ],
        inplace=True,
        ignore_index=True
    )

    # Column selection
    if select_columns==None:
        return df
    else:
        return df[select_columns]


# ____
# Maps

# Get 'Stadia Maps' provider through env variable
def get_stadiamaps_provider_api_key_in_env():
    
    # Find `.env` file and load var `STADIA_MAPS_API_KEY`
    load_dotenv(find_dotenv())
    stadia_maps_api_key = os.getenv('STADIA_MAPS_API_KEY')
    
    # AddAPI key to the style from contextily providers
    provider = cx.providers.Stadia.AlidadeSmooth(api_key=stadia_maps_api_key)
    
    # Update the provider URL to include your API key
    provider["url"] = provider["url"] + "?api_key={api_key}"

    return provider

# Function for basic elements in map plots
def general_map_style_plot(func):
    def wrapper(*args, **kwargs):
        fig, ax = func(*args, **kwargs)
        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        # Remove ticks
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        return fig, ax
    return wrapper

# Basic map plot function
@general_map_style_plot
def geo_plot_basic(df, provider, ax=None, color='blue'):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    else:
        fig = ax.figure  # Get the figure from the existing axis
    df.plot(ax=ax, alpha=0.5, color=color)
    cx.add_basemap(ax, crs=df.crs, source=provider)
    return fig, ax


# ______
# MLflow

# Get tracking URI
def get_mlflow_tracking_uri():
    
    # Find `.env` file and load var 'MLFLOW_TRACKING_URI'
    load_dotenv(find_dotenv())
    mlflow_tracking_uri = os.getenv('MLFLOW_TRACKING_URI')

    return mlflow_tracking_uri
