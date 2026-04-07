import logging
from pathlib import Path

def setup_logger(log_file="results/logs/validation.log"):
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("validation")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(log_file, mode="w")
        formatter = logging.Formatter(
            "%(asctime)s - %(message)s"
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger