import pandas as pd
import pytest

from src.drop_columns import drop_columns


def test_drop_columns_removes_requested_columns():
    """The returned DataFrame should exclude the requested columns only."""
    data_frame = pd.DataFrame(
        {
            "pha": [0, 1],
            "epoch": [2451545.0, 2451546.0],
            "abs_magnitude": [21.1, 22.4],
            "feature_x": [0.2, 0.8],
        }
    )

    result = drop_columns(data_frame, ["epoch", "abs_magnitude"])

    assert list(result.columns) == ["pha", "feature_x"]
    assert list(data_frame.columns) == ["pha", "epoch", "abs_magnitude", "feature_x"]


def test_drop_columns_returns_empty_dataframe_when_all_columns_removed():
    """The function should support dropping every column from a DataFrame."""
    data_frame = pd.DataFrame(
        {
            "pha": [0, 1],
            "feature_x": [0.2, 0.8],
        }
    )

    result = drop_columns(data_frame, ["pha", "feature_x"])

    assert result.empty
    assert list(result.columns) == []


def test_drop_columns_raises_type_error_for_non_dataframe_input():
    """The function should reject inputs that are not pandas DataFrames."""
    with pytest.raises(TypeError, match="data_frame must be a pandas DataFrame"):
        drop_columns(["pha", "epoch"], ["epoch"])


def test_drop_columns_raises_type_error_for_non_list_columns_argument():
    """The function should require column names to be provided as a list."""
    data_frame = pd.DataFrame(
        {
            "pha": [0, 1],
            "epoch": [2451545.0, 2451546.0],
        }
    )

    with pytest.raises(TypeError, match="columns must be provided as a list of strings"):
        drop_columns(data_frame, "epoch")


def test_drop_columns_raises_key_error_for_missing_columns():
    """The function should raise an error if a requested column does not exist."""
    data_frame = pd.DataFrame(
        {
            "pha": [0, 1],
            "feature_x": [0.2, 0.8],
        }
    )

    with pytest.raises(KeyError):
        drop_columns(data_frame, ["missing_column"])
