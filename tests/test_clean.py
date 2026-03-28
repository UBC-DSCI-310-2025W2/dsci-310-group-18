import pytest
import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clean import clean_pha, clean_full_name

# Tests for clean_pha
# Expected use cases
# test clean_pha function can map valid values to numeric
def test_clean_pha_basic_mapping():
    df = pd.DataFrame({'pha' : ['Y', 'N', 'Y']})
    result = clean_pha(df)

    assert result['pha'].tolist() == [1, 0, 1]

# test clean_pha function preserves other columns
def test_clean_pha_preserves_cols():
    df = pd.DataFrame({
        'pha': ['Y', 'N'],
        'moid': [10, 20]
    })
    result = clean_pha(df)

    assert 'moid' in result.columns
    assert result['moid'].tolist() == [10, 20]
    assert result['pha'].tolist() == [1, 0]

# Edge cases
# test clean_pha function returns an empty dataframe if 
# input dataframe is empty
def test_clean_pha_empty_df():
    df = pd.DataFrame({'pha': []})
    result = clean_pha(df)

    assert result.empty

# test clean_pha function handles normalization
def test_clean_pha_handles_lowercase_whitespace():
    df = pd.DataFrame({'pha': ['y', ' n ', 'Y']})
    result = clean_pha(df)

    assert result['pha'].tolist() == [1, 0, 1]

# Error cases
# test clean_pha function throws an error with invalid 
# input values in 'pha' column
def test_clean_pha_error_on_invalid_values():
    df = pd.DataFrame({'pha': ['Y', 'N', 'X']})

    with pytest.raises(ValueError):
        clean_pha(df)

def test_clean_pha_error_on_nan_values():
    df = pd.DataFrame({'pha': ['Y', None]})

    with pytest.raises(ValueError):
        clean_pha(df)

# Test for clean_full_name
# Expected use cases
# test clean_full_name function correctly removes parentheses
# and replaces spaces with underscore
def test_clean_full_name_parentheses():
    df = pd.DataFrame({'full_name': ['Asteroid (1234)']})
    result = clean_full_name(df)

    assert result['full_name'].iloc[0] == 'Asteroid_1234'

# test clean_full_name handles multiple spaces
# with only one underscore
def test_clean_full_name_multiple_spaces():
    df = pd.DataFrame({'full_name': ['Asteroid   1234']})
    result = clean_full_name(df)

    assert result['full_name'].iloc[0] == 'Asteroid_1234'

# Edge cases
# test clean_full_name removes leading and trailing spaces
def test_clean_full_name_leading_trailing_spaces():
    df = pd.DataFrame({'full_name': ['   (Asteroid 1234)   ']})
    result = clean_full_name(df)

    assert result['full_name'].iloc[0] == 'Asteroid_1234'

# test clean_full_name returns empty string given empty input string
def test_clean_full_name_empty_string():
    df = pd.DataFrame({'full_name': ['']})
    result = clean_full_name(df)

    assert result['full_name'].iloc[0] == ''

# Error cases
# test clean_full_name throws an error on a non-string value
def test_clean_full_name_non_string():
    df = pd.DataFrame({'full_name': ['Asteroid (1234)', 10]})

    with pytest.raises(ValueError, match='The column contains invalid values.'):
        clean_full_name(df)

# test clean_full_name throws an error on a NaN value
def test_clean_full_name_nan_values():
    df = pd.DataFrame({'full_name': ['Asteroid (1234)', None]})

    with pytest.raises(ValueError):
        clean_full_name(df)