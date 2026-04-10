import pandas as pd
import pytest
from src.validation import run_validation

def test_valid_data(tmp_path):
    """Validation should pass for a schema-compliant one-row dataset."""
    df = pd.DataFrame({
        "spkid": [20000433],
        "full_name": ["433_Eros_A898_PA"],
        "pdes": ["433"],
        "orbit_id": ["JPL 659"],
        "pha": [0],
        "min_orbit_intersection_dist": [57.7],
        "epoch": [2461000.5],
        "eccentricity": [0.2228],
        "semi_major_axis": [1.458],
        "perihelion_dist": [1.133],
        "inclination": [10.83],
        "mean_anomaly": [310.55],
        "time_of_perihelion_passage": [2461088.83],
        "abs_magnitude": [10.39]
    })

    file = tmp_path / "valid.csv"
    df.to_csv(file, index=False)

    result = run_validation(file)

    assert result is not None
    assert len(result) == 1 # No rows should be dropped

def test_invalid_data_schema(tmp_path):
    """Validation should fail when types, names, or values are invalid."""
    df = pd.DataFrame({
        "spkid": ["20000433"], # invalid data type
        "fullname": ["433_Eros_A898_PA"], # invalid column name
        "pdes": [None], # missigness
        "orbit_id": ["JPL 659"],
        "pha": ["yes"], # invalid category level
        "min_orbit_intersection_dist": [280], # value out of range
        "epoch": [None], # missingness
        "eccentricity": [0.2228],
        "semi_major_axis": [1.458],
        "perihelion_dist": [1.133],
        "inclination": [10.83],
        "mean_anomaly": [310.55],
        "time_of_perihelion_passage": [2461088.83],
        "abs_magnitude": [10.39]
    })

    file = tmp_path / "invalid.csv"
    df.to_csv(file, index=False)
    
    with pytest.raises(Exception):
        run_validation(file)

def test_duplicate_rows(tmp_path):
    """Validation should reject duplicated observations."""
    df = pd.DataFrame({
        "spkid": [20000433, 20000433],
        "full_name": ["433_Eros_A898_PA", "433_Eros_A898_PA"],
        "pdes": ["433", "433"],
        "orbit_id": ["JPL 659", "JPL 659"],
        "pha": [0, 0],
        "min_orbit_intersection_dist": [57.7, 57.7],
        "epoch": [2461000.5, 2461000.5],
        "eccentricity": [0.2228, 0.2228],
        "semi_major_axis": [1.458, 1.458],
        "perihelion_dist": [1.133, 1.133],
        "inclination": [10.83, 10.83],
        "mean_anomaly": [310.55, 310.55],
        "time_of_perihelion_passage": [2461088.83, 2461088.83],
        "abs_magnitude": [10.39, 10.39]
    })

    file = tmp_path / "dup.csv"
    df.to_csv(file, index=False)

    with pytest.raises(Exception):
        run_validation(file)

def test_outliers(tmp_path):
    """Validation should reject rows that violate numeric bounds."""
    df = pd.DataFrame({
        "spkid": [20000433],
        "full_name": ["433_Eros_A898_PA"],
        "pdes": ["433"],
        "orbit_id": ["JPL 659"],
        "pha": [0],
        "min_orbit_intersection_dist": [1000], # outlier
        "epoch": [2461000.5],
        "eccentricity": [0.2228],
        "semi_major_axis": [1.458],
        "perihelion_dist": [1.133],
        "inclination": [10.83],
        "mean_anomaly": [310.55],
        "time_of_perihelion_passage": [2461088.83],
        "abs_magnitude": [10.39]
    })

    file = tmp_path / "outlier.csv"
    df.to_csv(file, index=False)

    with pytest.raises(Exception):
        run_validation(file)

def test_invalid_file_format(tmp_path):
    """Validation should reject unsupported input file formats."""
    file = tmp_path / "data.txt"
    file.write_text("invalid content")

    with pytest.raises(ValueError):
        run_validation(file)
