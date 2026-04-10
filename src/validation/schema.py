import pandera as pa
from pandera import Column, DataFrameSchema, Check

def get_schema():
    """
    Returns DataFrameSchema for pandera checks
    - Based on the cleaned dataset
    - Covers column names, data types, category levels, and basic values,
    - And duplicate rows and empty rows
    """
    return DataFrameSchema({
        "spkid": Column(int, unique=True),
        "full_name": Column(str),
        "pdes": Column(str),
        "orbit_id": Column(str),
        "pha": Column(int, Check.isin([0, 1])),
        "min_orbit_intersection_dist": Column(float, Check.between(0.000177, 276.0)),
        "epoch": Column(float, Check.between(2444221.5, 2462000.5)), # I changed the epoch range from 2461119.5 to 2462000.5
        "eccentricity": Column(float, Check.between(0.0028, 0.9964)),
        "semi_major_axis": Column(float, Check.between(0.4618, 350.3)),
        "perihelion_dist": Column(float, Check.between(0.069, 1.3)),
        "inclination": Column(float, Check.between(0.01, 165.6)),
        "mean_anomaly": Column(float, Check.between(0.0, 360.0)),
        "time_of_perihelion_passage": Column(float, Check.between(2444267.67, 2462387.16)),
        "abs_magnitude": Column(float, Check.between(9.17, 34.06))
    },
        strict=True,
        coerce=True,
        checks=[
            Check(lambda df: ~df.duplicated().any(), error="Duplicate rows"),
            Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows")
        ],
        drop_invalid_rows=False
    )