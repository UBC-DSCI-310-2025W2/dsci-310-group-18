"""Fetch near-Earth asteroid records from the NASA JPL SBDB API.

This command-line script downloads the raw dataset used throughout the
analysis pipeline and writes it to a CSV file.

Example
-------
python scripts/01_fetch-data.py \
    --read-url="https://ssd-api.jpl.nasa.gov/sbdb_query.api" \
    --write-path=data/raw/asteroid_data_raw.csv
"""

import click
import requests
import pandas as pd
from pathlib import Path

@click.command()
@click.option('--read-url', type=str, help='Base URL of data to be downloaded.')
@click.option('--write-path', type=str, help='Filepath where raw data will be written.')

def main(read_url, write_path):
    """Sends request to NASA's JPL SBDB Query API, downloads data, and writes to CSV."""

    fields = [
        "spkid", "full_name", "pdes", "orbit_id",
        "pha", "moid_ld", "epoch",
        "e", "a", "q", "i", "ma", "tp", "H",
    ]
    
    params = {
        "sb-kind": "a",
        "sb-group": "neo", # near earth objects only
        "fields": ",".join(fields)
    }
    
    try:
        response = requests.get(read_url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to download data from API: {e}")
    
    data = response.json()
    records = data.get("data", [])

    df = pd.DataFrame(records, columns=fields)

    Path(write_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(write_path, index=False)

if __name__ == '__main__':
    main()
