"""Split the validated dataset and fit the preprocessing transformer.

This command-line script performs the train/validation/test split used by the
project, applies robust scaling, and saves the processed datasets and scaler.

Example
-------
python scripts/04_split-data.py \
    --clean-data-path=data/validated/asteroid_data_validated.csv \
    --output-dir=data/processed
"""

import click
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
import joblib
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.split_features_target import split_features_target

@click.command()
@click.option('--clean-data-path', type=str, required=True, help='Filepath to clean data.')
@click.option('--output-dir', type=str, required=True, help='Directory to write preprocessed data splits.')
@click.option('--seed', default=123, type=int, help='Random seed for reproducing data splits.')

def main(clean_data_path, output_dir, seed):
    """Splits cleaned data into train/val/test and applies RobustScaler."""
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(clean_data_path)

    # Features and target
    X, y = split_features_target(df)

    # Train (60%) / Test (20%)
    X_temp, X_test, y_temp, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=seed
    )

    # Train (60%) / Val (20%)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp,
        y_temp,
        test_size=0.25,
        stratify=y_temp,
        random_state=seed
    )

    # Fit RobustScaler on training only
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # Transform val/test with RobustScaler
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    # Convert back to dataframes
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_val_scaled = pd.DataFrame(X_val_scaled, columns=X_val.columns, index=X_val.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)

    # Reattach target
    train_df = pd.concat([X_train_scaled, y_train], axis=1)
    val_df = pd.concat([X_val_scaled, y_val], axis=1)
    test_df = pd.concat([X_test_scaled, y_test], axis=1)

    # Save data
    train_df.to_csv(f"{output_dir}/asteroid_train.csv", index=False)
    val_df.to_csv(f"{output_dir}/asteroid_val.csv", index=False)
    test_df.to_csv(f"{output_dir}/asteroid_test.csv", index=False)

    # Save scaler
    joblib.dump(scaler, f"{output_dir}/robust_scaler.pkl")

if __name__ == '__main__':
    main()
