import pandas as pd
import pytest

from src.prepare_eval_data import prepare_eval_data

## Expected use cases
# test basic evaluation data split
def test_prepare_eval_data_basic():
    df = pd.DataFrame(
        {
            "pha": [0, 1],
            "abs_magnitude": [21.1, 22.3],
            "epoch": [2451545.0, 2451546.0],
            "min_orbit_intersection_dist": [0.01, 0.02],
            "semi_major_axis": [1.2, 1.4],
            "time_of_perihelion_passage": [12345.0, 12346.0],
            "eccentricity": [0.2, 0.3],
            "inclination": [5.1, 6.2],
        }
    )

    X, y = prepare_eval_data(df)

    assert list(X.columns) == ["eccentricity", "inclination"]
    assert X.shape == (2, 2)
    assert y.tolist() == [0, 1]


# test dropped columns are not included in X
def test_prepare_eval_data_drops_expected_columns():
    df = pd.DataFrame(
        {
            "pha": [0, 1],
            "abs_magnitude": [21.1, 22.3],
            "epoch": [2451545.0, 2451546.0],
            "min_orbit_intersection_dist": [0.01, 0.02],
            "semi_major_axis": [1.2, 1.4],
            "time_of_perihelion_passage": [12345.0, 12346.0],
            "moid_ld": [4.0, 5.0],
        }
    )

    X, y = prepare_eval_data(df)

    assert "pha" not in X.columns
    assert "abs_magnitude" not in X.columns
    assert "epoch" not in X.columns
    assert "min_orbit_intersection_dist" not in X.columns
    assert "semi_major_axis" not in X.columns
    assert "time_of_perihelion_passage" not in X.columns
    assert y.name == "pha"


## Edge cases
# test X is empty if only dropped columns are present
def test_prepare_eval_data_empty_X():
    df = pd.DataFrame(
        {
            "pha": [0, 1],
            "abs_magnitude": [21.1, 22.3],
            "epoch": [2451545.0, 2451546.0],
            "min_orbit_intersection_dist": [0.01, 0.02],
            "semi_major_axis": [1.2, 1.4],
            "time_of_perihelion_passage": [12345.0, 12346.0],
        }
    )

    X, y = prepare_eval_data(df)

    assert X.empty
    assert list(X.columns) == []
    assert y.tolist() == [0, 1]


## Error cases
# test error is raised for non-dataframe input
def test_prepare_eval_data_non_dataframe():
    with pytest.raises(TypeError, match="df must be a pandas DataFrame"):
        prepare_eval_data(["not", "a", "dataframe"])


# test error is raised when pha column is missing
def test_prepare_eval_data_missing_pha():
    df = pd.DataFrame(
        {
            "abs_magnitude": [21.1, 22.3],
            "epoch": [2451545.0, 2451546.0],
            "min_orbit_intersection_dist": [0.01, 0.02],
            "semi_major_axis": [1.2, 1.4],
            "time_of_perihelion_passage": [12345.0, 12346.0],
            "eccentricity": [0.2, 0.3],
        }
    )

    with pytest.raises(KeyError, match="Missing required columns"):
        prepare_eval_data(df)


# test error is raised when a dropped column is missing
def test_prepare_eval_data_missing_drop_column():
    df = pd.DataFrame(
        {
            "pha": [0, 1],
            "abs_magnitude": [21.1, 22.3],
            "epoch": [2451545.0, 2451546.0],
            "min_orbit_intersection_dist": [0.01, 0.02],
            "semi_major_axis": [1.2, 1.4],
            "eccentricity": [0.2, 0.3],
        }
    )

    with pytest.raises(KeyError, match="Missing required columns"):
        prepare_eval_data(df)