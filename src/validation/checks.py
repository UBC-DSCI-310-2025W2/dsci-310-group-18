# Dataframe level checks

import numpy as np
from pathlib import Path

NUMERIC_COL_BOUNDS = {
    "moid_ld": (0.000177, 276.0),
    "epoch": (2444221.5, 2461119.5),
    "e": (0.0028, 0.9964),
    "a": (0.4618, 350.3),
    "q": (0.069, 1.3),
    "i": (0.01, 165.6),
    "ma": (0.0, 360.0),
    "tp": (2444267.67, 2462387.16),
    "H": (9.17, 34.06)
}

def check_file_format(file_path):
    file_path = Path(file_path)
    if file_path.suffix != ".csv":
        raise ValueError("File must be a CSV.")

def check_missingness(df, threshold=0.2):
    if df.empty:
        return True # Nothing missing in empty df
    return (df.isnull().mean() < threshold).all()

def check_no_duplicates(df):
    return ~df.duplicated().any()

def check_no_outliers(df):
    for col, (lo, hi) in NUMERIC_COL_BOUNDS.items():
        if col in df.columns:
            if not df[col].dropna().between(lo, hi).all():
                return False
    return True