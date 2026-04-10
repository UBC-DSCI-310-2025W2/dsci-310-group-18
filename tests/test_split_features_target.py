import pandas as pd
import pytest

from src.split_features_target import split_features_target

def test_split_features_target_basic():
    """The helper should split target values from numeric predictors."""
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

def test_split_features_target_drops_pha_and_spkid():
    """The helper should exclude identifier and target columns from X."""
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

def test_split_features_target_numeric_only():
    """The helper should retain only numeric predictor columns."""
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

def test_split_features_target_empty_X():
    """The helper should allow an empty feature matrix when needed."""
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

def test_split_features_target_non_dataframe():
    """The helper should reject inputs that are not DataFrames."""
    with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
        split_features_target(["not", "a", "dataframe"])

def test_split_features_target_missing_pha():
    """The helper should require the target column."""
    df = pd.DataFrame(
        {
            "spkid": [1, 2],
            "moid": [0.1, 0.2],
        }
    )

    with pytest.raises(KeyError, match="Missing required columns"):
        split_features_target(df)

def test_split_features_target_missing_spkid():
    """The helper should require the asteroid identifier column."""
    df = pd.DataFrame(
        {
            "pha": [0, 1],
            "moid": [0.1, 0.2],
        }
    )

    with pytest.raises(KeyError, match="Missing required columns"):
        split_features_target(df)
