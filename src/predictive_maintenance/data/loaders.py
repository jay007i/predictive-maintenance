"""Functions for loading raw NASA C-MAPSS data files."""

from pathlib import Path

import pandas as pd

from predictive_maintenance.constants import RAW_COLUMN_NAMES


def load_cmapss_data(file_path: str | Path) -> pd.DataFrame:
    """Load and validate a whitespace-separated NASA C-MAPSS data file.

    Args:
        file_path: Path to a headerless C-MAPSS text file.

    Returns:
        A DataFrame with the shared 26-column C-MAPSS schema.

    Raises:
        FileNotFoundError: If ``file_path`` does not exist.
        ValueError: If the path is not a file, the file is empty, cannot be
            parsed as numeric data, or does not contain 26 columns.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"C-MAPSS data file not found: {path}")

    if not path.is_file():
        raise ValueError(f"C-MAPSS data path is not a file: {path}")

    try:
        data = pd.read_csv(path, sep=r"\s+", header=None)
    except pd.errors.EmptyDataError as error:
        raise ValueError(f"C-MAPSS data file is empty: {path}") from error
    except (OSError, pd.errors.ParserError) as error:
        raise ValueError(f"Unable to parse C-MAPSS data file: {path}") from error

    if data.empty:
        raise ValueError(f"C-MAPSS data file is empty: {path}")

    expected_column_count = len(RAW_COLUMN_NAMES)
    if data.shape[1] != expected_column_count:
        raise ValueError(
            "Malformed C-MAPSS data file "
            f"{path}: expected {expected_column_count} columns, found {data.shape[1]}."
        )

    try:
        data = data.apply(pd.to_numeric, errors="raise")
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"Malformed C-MAPSS data file {path}: all values must be numeric."
        ) from error

    data.columns = RAW_COLUMN_NAMES
    return data
