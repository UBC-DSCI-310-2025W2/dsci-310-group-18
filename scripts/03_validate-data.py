# 02_validate-data.py
# Author: Sadie Lee
# date: 2026-04-07

import click
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.validation import run_validation

@click.command()
@click.option("--clean-data-path", type=str, help="Path to clean data file", required=True)
@click.option("--validated-data-path", type=str, help="Path to validated data file", required=True)

def main(clean_data_path, validated_data_path):
    try:
        validated = run_validation(clean_data_path, log_file="results/logs/validation.log")
        print(f"Rows after val: {validated.shape[0]}")
        validated.to_csv(validated_data_path, index=False)
    except Exception as e:
       print(f"Validation failed: {e}")
       raise

if __name__ == "__main__":
    main()