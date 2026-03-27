import pandas as pd
import pytest

from src.split_features_target import split_features_target


def test_split_features_target_returns_expected_X_and_y():
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


def test_split_features_target_excludes_pha_and_spkid_from_X():
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


def test_split_features_target_keeps_only_numeric_predictors():
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


def test_split_features_target_returns_empty_X_if_no_numeric_predictors_remain():
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


def test_split_features_target_raises_type_error_for_non_dataframe_input():
    with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
        split_features_target(["not", "a", "dataframe"])


def test_split_features_target_raises_key_error_when_pha_missing():
    df = pd.DataFrame(
        {
            "spkid": [1, 2],
            "moid": [0.1, 0.2],
        }
    )

    with pytest.raises(KeyError, match="Missing required columns"):
        split_features_target(df)


def test_split_features_target_raises_key_error_when_spkid_missing():
    df = pd.DataFrame(
        {
            "pha": [0, 1],
            "moid": [0.1, 0.2],
        }
    )

    with pytest.raises(KeyError, match="Missing required columns"):
        split_features_target(df)