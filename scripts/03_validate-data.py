"""Validate the cleaned asteroid dataset against schema and quality checks.

This command-line script runs the validation subpackage, logs validation
results, and writes the validated dataset to disk if checks pass.

Example
-------
python scripts/03_validate-data.py \
    --clean-data-path=data/clean/asteroid_data_clean.csv \
    --validated-data-path=data/validated/asteroid_data_validated.csv
"""

import click
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.validation import run_validation

@click.command()
@click.option("--clean-data-path", type=str, help="Path to clean data file", required=True)
@click.option("--validated-data-path", type=str, help="Path to validated data file", required=True)

def main(clean_data_path, validated_data_path):
    """Run validation and persist the validated dataset."""
    try:
        validated = run_validation(clean_data_path, log_file="results/logs/validation.log")
        print(f"Rows after val: {validated.shape[0]}")
        validated.to_csv(validated_data_path, index=False)
    except Exception as e:
       print(f"Validation failed: {e}")
       raise

if __name__ == "__main__":
    main()
