import pytest
import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clean import clean_pha, clean_full_name

def test_clean_pha_basic_mapping():
    """`clean_pha` should map valid hazard labels to 1/0."""
    df = pd.DataFrame({'pha' : ['Y', 'N', 'Y']})
    result = clean_pha(df)

    assert result['pha'].tolist() == [1, 0, 1]

def test_clean_pha_preserves_cols():
    """`clean_pha` should preserve non-target columns unchanged."""
    df = pd.DataFrame({
        'pha': ['Y', 'N'],
        'moid': [10, 20]
    })
    result = clean_pha(df)

    assert 'moid' in result.columns
    assert result['moid'].tolist() == [10, 20]
    assert result['pha'].tolist() == [1, 0]

def test_clean_pha_empty_df():
    """`clean_pha` should support empty DataFrames."""
    df = pd.DataFrame({'pha': []})
    result = clean_pha(df)

    assert result.empty

def test_clean_pha_handles_lowercase_whitespace():
    """`clean_pha` should normalize case and surrounding whitespace."""
    df = pd.DataFrame({'pha': ['y', ' n ', 'Y']})
    result = clean_pha(df)

    assert result['pha'].tolist() == [1, 0, 1]

def test_clean_pha_error_on_invalid_values():
    """`clean_pha` should reject unexpected target labels."""
    df = pd.DataFrame({'pha': ['Y', 'N', 'X']})

    with pytest.raises(ValueError):
        clean_pha(df)

def test_clean_pha_error_on_nan_values():
    """`clean_pha` should reject missing target values."""
    df = pd.DataFrame({'pha': ['Y', None]})

    with pytest.raises(ValueError):
        clean_pha(df)

def test_clean_full_name_parentheses():
    """`clean_full_name` should remove parentheses and normalize spaces."""
    df = pd.DataFrame({'full_name': ['Asteroid (1234)']})
    result = clean_full_name(df)

    assert result['full_name'].iloc[0] == 'Asteroid_1234'

def test_clean_full_name_multiple_spaces():
    """`clean_full_name` should collapse repeated spaces to one underscore."""
    df = pd.DataFrame({'full_name': ['Asteroid   1234']})
    result = clean_full_name(df)

    assert result['full_name'].iloc[0] == 'Asteroid_1234'

def test_clean_full_name_leading_trailing_spaces():
    """`clean_full_name` should strip leading and trailing separators."""
    df = pd.DataFrame({'full_name': ['   (Asteroid 1234)   ']})
    result = clean_full_name(df)

    assert result['full_name'].iloc[0] == 'Asteroid_1234'

def test_clean_full_name_empty_string():
    """`clean_full_name` should preserve an empty string input."""
    df = pd.DataFrame({'full_name': ['']})
    result = clean_full_name(df)

    assert result['full_name'].iloc[0] == ''

def test_clean_full_name_non_string():
    """`clean_full_name` should reject non-string entries."""
    df = pd.DataFrame({'full_name': ['Asteroid (1234)', 10]})

    with pytest.raises(ValueError, match='The column contains invalid values.'):
        clean_full_name(df)

def test_clean_full_name_nan_values():
    """`clean_full_name` should reject missing values."""
    df = pd.DataFrame({'full_name': ['Asteroid (1234)', None]})

    with pytest.raises(ValueError):
        clean_full_name(df)
