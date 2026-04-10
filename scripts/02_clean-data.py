"""Clean the raw asteroid dataset and write the cleaned output to disk.

This command-line script renames columns, standardizes the target and
asteroid names, removes invalid rows, and saves the cleaned dataset.

Example
-------
python scripts/02_clean-data.py \
    --raw-data-path=data/raw/asteroid_data_raw.csv \
    --clean-data-path=data/clean/asteroid_data_clean.csv
"""

import click
import pandas as pd
from asteroidprep import clean_pha, clean_full_name

@click.command()
@click.option('--raw-data-path', type=str, help='Filepath to raw data.')
@click.option('--clean-data-path', type=str, help='Filepath to write clean data.')

def main(raw_data_path, clean_data_path):
    """Cleans raw data, writes clean data to CSV."""

    df = pd.read_csv(raw_data_path)

    # Rename columns
    df = df.rename(columns={
        'moid_ld': 'min_orbit_intersection_dist',
        'e': 'eccentricity',
        'a': 'semi_major_axis',
        'q': 'perihelion_dist',
        'i': 'inclination',
        'ma': 'mean_anomaly',
        'tp': 'time_of_perihelion_passage',
        'H': 'abs_magnitude'
    })

    # Drop rows where PHA (target) is NaN
    df.dropna(subset=['pha'], inplace=True)

    # Convert PHA to boolean
    df = clean_pha(df)

    # Clean and standardize full name
    df = clean_full_name(df)

    # Drop rows where absolute magnitude is NaN
    df.dropna(subset=['abs_magnitude'], inplace=True)

    # Save clean data
    df.to_csv(clean_data_path, index=False)

if __name__ == '__main__':
    main()
