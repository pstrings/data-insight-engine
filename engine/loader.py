import pandas as pd

from engine.logger import get_logger
from typing import Optional
from pathlib import Path


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.
    """
    logger = get_logger()
    path = Path(file_path)

    if not path.exists():
        logger.error(f"File does not exist: {file_path}")
        raise FileNotFoundError(f"{file_path} not found")

    if path.suffix.lower() != ".csv":
        logger.error(f"Invalid file format: {file_path}")
        raise ValueError("Only CSV files are supported")

    try:
        try:
            data: pd.DataFrame = pd.read_csv(path, encoding="utf-8")
        except UnicodeDecodeError:
            logger.warning("UTF-8 failed, retrying with latin1 encoding")
            data: pd.DataFrame = pd.read_csv(path, encoding="latin1")

        logger.info(
            f"Dataset loaded successfully | rows={data.shape[0]} | columns={data.shape[1]}")

        return data
    except pd.errors.EmptyDataError:
        logger.exception("CSV file is empty")
        raise

    except pd.errors.ParserError:
        logger.exception("CSV parsing failed")
        raise
    except Exception as e:
        logger.exception(e)
        raise
