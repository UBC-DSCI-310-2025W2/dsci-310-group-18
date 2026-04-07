import pandas as pd
import pandera as pa
from pandera.errors import SchemaError, SchemaErrors

from .schema import get_schema
from .checks import (
    check_file_format,
    check_missingness,
    check_no_duplicates,
    check_no_outliers
)
from .logging import setup_logger

def run_validation(file_path, log_file="validation.log"):
    logger = setup_logger()

    # File format
    check_file_format(file_path)
    logger.info("File format check passed.")

    # Load data
    data = pd.read_csv(file_path)

    # Schema checks:
        # Column names
        # Data types
        # Category levels
        # Basic value ranges
        # Duplicate rows
        # Empty rows
    schema = get_schema()
    error_cases = None
    try:
        validated_data = schema.validate(data, lazy=True)
        logger.info("Schema validation passed.")
    except (SchemaError, SchemaErrors) as e:
        error_cases = e.failure_cases if hasattr(e, "failure_cases") else None
        if error_cases is not None:
            logger.error(f"Validation failed with {len(error_cases)} errors")
            logger.error(error_cases.head().to_string())
        raise

    # Outliers
    assert check_no_outliers(data), "Extreme outliers found."
    logger.info("Outlier check passed.")

    # Drop missing
    assert check_missingness(data), "Too many missing values."
    logger.info("Missingness check passed.")

    # No duplicates
    assert check_no_duplicates(data), "Duplicate rows found."
    logger.info("Duplicates check passed.")

    logger.info("All validation checks passed.")

    return data # return unchanged