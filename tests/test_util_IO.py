import os
import sys
import pandas as pd
from pandas.testing import assert_frame_equal
from unittest.mock import MagicMock, mock_open

# Add src to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from util_IO import (
    get_use_case_main_dir,
    load_pickle_from_main_project_dir,
    EDA_dirs_structure,
    load_attributes_df,
    load_timeseries_df,
    get_stadiamaps_provider_api_key_in_env,
    get_mlflow_tracking_uri
)

def test_get_use_case_main_dir(mocker):
    # Store original functions
    original_basename = os.path.basename
    original_dirname = os.path.dirname

    # Mock the file system functions
    mocker.patch('os.path.abspath', return_value='/fake/dir/Open-Flow-Model/notebooks')
    
    # Use real os.path.basename and os.path.dirname logic
    def basename_side_effect(path):
        return original_basename(path)

    def dirname_side_effect(path):
        return original_dirname(path)

    mocker.patch('os.path.basename', side_effect=basename_side_effect)
    mocker.patch('os.path.dirname', side_effect=dirname_side_effect)

    # Expected result
    expected_dir = '/fake/dir/Open-Flow-Model'
    
    # Call the function
    result_dir = get_use_case_main_dir()
    
    # Assert the result
    assert result_dir == expected_dir

def test_load_pickle_from_main_project_dir(mocker):
    # Mock dependencies
    mocker.patch('util_IO.get_use_case_main_dir', return_value='/fake/dir')
    mock_file = mocker.patch('builtins.open', mock_open(read_data=b'test_pickle_data'))
    mock_pickle = mocker.patch('pickle.load', return_value="pickle_content")

    # Call the function
    content, directory = load_pickle_from_main_project_dir('test.pkl')

    # Assertions
    mock_file.assert_called_with('/fake/dir/test.pkl', 'rb')
    assert content == "pickle_content"
    assert directory == '/fake/dir'

def test_EDA_dirs_structure(mocker):
    # Mock the main directory
    mocker.patch('util_IO.get_use_case_main_dir', return_value='/fake/dir')

    # Expected paths
    expected_eda_dir = '/fake/dir/resources/EDA'
    expected_attributes_dir = '/fake/dir/resources/EDA/attributes'
    expected_timeseries_dir = '/fake/dir/resources/EDA/timeseries'

    # Call the function
    eda_dir, attributes_dir, timeseries_dir = EDA_dirs_structure()

    # Assertions
    assert eda_dir == expected_eda_dir
    assert attributes_dir == expected_attributes_dir
    assert timeseries_dir == expected_timeseries_dir

def test_load_attributes_df(mocker):
    # Create a dummy DataFrame
    dummy_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]}, index=['a', 'b'])
    mock_read_csv = mocker.patch('pandas.read_csv', return_value=dummy_df)

    # Call the function
    df = load_attributes_df('/fake/dir', 'test.csv', 'index_col')

    # Assertions
    mock_read_csv.assert_called_with('/fake/dir/test.csv', dtype={'index_col': 'str'}, index_col='index_col')
    assert_frame_equal(df, dummy_df)

def test_load_timeseries_df(mocker):
    # Create a dummy DataFrame
    dummy_df = pd.DataFrame({
        'catchmentID': ['1', '1', '2'],
        'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-01']),
        'value': [10, 20, 30]
    })
    mock_read_csv = mocker.patch('pandas.read_csv', return_value=dummy_df.copy())

    # Call the function
    df = load_timeseries_df('/fake/dir', 'test.csv', 'date')

    # Assertions
    mock_read_csv.assert_called_with('/fake/dir/test.csv', dtype={"catchmentID": 'str'}, parse_dates=['date'])
    assert 'date' in df.columns

def test_get_stadiamaps_provider_api_key_in_env(mocker):
    # Mock environment variable
    mocker.patch.dict(os.environ, {'STADIA_MAPS_API_KEY': 'test_api_key'})
    
    # Mock contextily provider
    mock_provider_instance = MagicMock()
    # Set up the mock to behave like a dictionary for item access
    type(mock_provider_instance).url = 'http://example.com'
    
    def get_item(key):
        if key == 'url':
            return mock_provider_instance.url
        return None

    def set_item(key, value):
        if key == 'url':
            mock_provider_instance.url = value

    mock_provider_instance.__getitem__.side_effect = get_item
    mock_provider_instance.__setitem__.side_effect = set_item

    mock_stadia_provider = mocker.patch('contextily.providers.Stadia.AlidadeSmooth', return_value=mock_provider_instance)

    # Call the function
    provider = get_stadiamaps_provider_api_key_in_env()

    # Assertions
    mock_stadia_provider.assert_called_with(api_key='test_api_key')
    assert provider.url == 'http://example.com?api_key={api_key}'

def test_get_mlflow_tracking_uri(mocker):
    # Mock environment variable
    mocker.patch.dict(os.environ, {'MLFLOW_TRACKING_URI': 'http://localhost:5000'})
    
    # Call the function
    uri = get_mlflow_tracking_uri()

    # Assertion
    assert uri == 'http://localhost:5000'
