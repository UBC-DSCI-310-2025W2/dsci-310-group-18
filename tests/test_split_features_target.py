import pandas as pd
import pytest

from src.split_features_target import split_features_target

## Expected use cases
# test basic feature and target split
def test_split_features_target_basic():
    df = pd.DataFrame(
        {
            "spkid": [101, 102, 103],
            "pha": [1, 0, 1],
            "moid": [0.05, 0.10, 0.15],
            "eccentricity": [0.2, 0.3, 0.4],
            "full_name": ["A", "B", "C"],
        }
    )

    X, y = split_features_target(df)

    assert list(X.columns) == ["moid", "eccentricity"]
    assert X.shape == (3, 2)
    assert y.tolist() == [1, 0, 1]

# test pha and spkid are removed from X
def test_split_features_target_drops_pha_and_spkid():
    df = pd.DataFrame(
        {
            "spkid": [1, 2],
            "pha": [0, 1],
            "moid": [0.1, 0.2],
        }
    )

    X, y = split_features_target(df)

    assert "pha" not in X.columns
    assert "spkid" not in X.columns
    assert y.name == "pha"

# test only numeric predictor columns are kept
def test_split_features_target_numeric_only():
    df = pd.DataFrame(
        {
            "spkid": [1, 2],
            "pha": [0, 1],
            "moid": [0.1, 0.2],
            "orbit_class": ["Apollo", "Aten"],
        }
    )

    X, _ = split_features_target(df)

    assert list(X.columns) == ["moid"]

## Edge cases
# test X is empty when no numeric predictors remain
def test_split_features_target_empty_X():
    df = pd.DataFrame(
        {
            "spkid": [1, 2],
            "pha": [0, 1],
            "full_name": ["A", "B"],
        }
    )

    X, y = split_features_target(df)

    assert X.empty
    assert list(X.columns) == []
    assert y.tolist() == [0, 1]

## Error cases
# test error is raised for non-dataframe input
def test_split_features_target_non_dataframe():
    with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
        split_features_target(["not", "a", "dataframe"])

# test error is raised when pha column is missing
def test_split_features_target_missing_pha():
    df = pd.DataFrame(
        {
            "spkid": [1, 2],
            "moid": [0.1, 0.2],
        }
    )

    with pytest.raises(KeyError, match="Missing required columns"):
        split_features_target(df)

# test error is raised when spkid column is missing
def test_split_features_target_missing_spkid():
    df = pd.DataFrame(
        {
            "pha": [0, 1],
            "moid": [0.1, 0.2],
        }
    )

    with pytest.raises(KeyError, match="Missing required columns"):
        split_features_target(df)