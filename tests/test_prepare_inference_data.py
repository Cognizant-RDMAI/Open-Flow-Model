import os
import sys
import pandas as pd
import numpy as np
import pytest
from unittest.mock import MagicMock

# Add src to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from prepare_inference_data import prepare_data_for_inference, load_pickle

@pytest.fixture
def mock_data():
    """Create mock timeseries and attributes data for testing."""
    # Timeseries data
    dates = pd.to_datetime(pd.date_range(start='2023-01-01', periods=40, freq='D'))
    ts_data = {
        'date': dates,
        'catchmentID': ['1'] * 40,
        'feature1': np.random.rand(40),
        'feature2': np.random.rand(40),
        'discharge_spec': np.random.rand(40)
    }
    timeseries_df = pd.DataFrame(ts_data)

    # Attribute data
    attr_data = {
        'catchmentID': ['1'],
        'static1': [10],
        'static2': [20]
    }
    attributes_df = pd.DataFrame(attr_data).set_index('catchmentID')
    
    return timeseries_df, attributes_df

@pytest.fixture
def mock_preprocessors():
    """Create mock preprocessor objects."""
    # Mock for timeseries preprocessor
    X_preprocessor = MagicMock()
    X_preprocessor.transform.side_effect = lambda x: x * 2  # Simple transformation for testing

    # Mock for static preprocessor
    X_static_preprocessor = MagicMock()
    X_static_preprocessor.transform.side_effect = lambda x: x + 5 # Simple transformation for testing

    model_feed = {
        'X_preprocessor': X_preprocessor,
        'X_static_preprocessor': X_static_preprocessor,
        'X_cols_names': ['feature1', 'feature2'],
        'X_static_cols_names': ['static1', 'static2'],
        'label_field_feed': 'discharge_spec'
    }
    return model_feed

def test_prepare_data_for_inference(mocker, mock_data, mock_preprocessors):
    # Unpack mock data
    timeseries_df, attributes_df = mock_data
    
    # Mock the load_pickle function
    mocker.patch('prepare_inference_data.load_pickle', return_value=mock_preprocessors)

    # --- Call the function under test ---
    X_inf, X_static_inf, y_inf, registry_inf = prepare_data_for_inference(
        timeseries_df,
        attributes_df,
        'dummy_path.pkl',
        sequence_length=30
    )

    # --- Assertions ---
    # Check shapes
    expected_sequences = len(timeseries_df) - 30 + 1
    assert X_inf.shape == (expected_sequences, 30, 2)  # (num_sequences, seq_length, num_features)
    assert X_static_inf.shape == (expected_sequences, 2) # (num_sequences, num_static_features)
    assert y_inf.shape == (expected_sequences,)
    assert registry_inf.shape == (expected_sequences, 3)

    # Check scaling application
    # Timeseries data should be multiplied by 2
    assert np.allclose(X_inf[0, 0, 0], timeseries_df['feature1'].iloc[0] * 2)
    # Static data should have 5 added
    assert np.allclose(X_static_inf['static1'].iloc[0], attributes_df['static1'].iloc[0] + 5)

    # Check registry content
    assert 'start_date' in registry_inf.columns
    assert 'end_date' in registry_inf.columns
    assert 'catchmentID' in registry_inf.columns
    assert registry_inf['catchmentID'].iloc[0] == '1'

def test_prepare_data_insufficient_data(mocker, mock_data, mock_preprocessors):
    # Use only a small slice of data
    timeseries_df, attributes_df = mock_data
    timeseries_df = timeseries_df.head(20)

    mocker.patch('prepare_inference_data.load_pickle', return_value=mock_preprocessors)

    # Expect a ValueError because no sequences can be created
    with pytest.raises(ValueError, match="No valid sequences could be created"):
        prepare_data_for_inference(
            timeseries_df,
            attributes_df,
            'dummy_path.pkl',
            sequence_length=30
        )

def test_load_pickle(mocker):
    # Mock the file opening and pickle loading
    mocker.patch('builtins.open', mocker.mock_open(read_data=b"test"))
    mock_pickle_load = mocker.patch('pickle.load', return_value={'key': 'value'})

    # Call the function
    result = load_pickle('dummy_path.pkl')

    # Assertions
    assert result == {'key': 'value'}
    mock_pickle_load.assert_called_once()
