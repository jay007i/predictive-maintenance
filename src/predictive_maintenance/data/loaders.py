"""Functions for loading raw NASA C-MAPSS data files."""

from pathlib import Path

import pandas as pd

from predictive_maintenance.constants import RAW_COLUMN_NAMES, RUL_COLUMN
from predictive_maintenance.data.validation import validate_cmapss_trajectory


def _validate_file_path(file_path: str | Path, data_name: str) -> Path:
    """Return an existing file path or raise a meaningful error."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{data_name} file not found: {path}")

    if not path.is_file():
        raise ValueError(f"{data_name} path is not a file: {path}")

    return path


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
    path = _validate_file_path(file_path, "C-MAPSS data")

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
    validate_cmapss_trajectory(data)
    return data


def load_rul_targets(file_path: str | Path) -> pd.Series:
    """Load official C-MAPSS remaining-useful-life labels.

    Args:
        file_path: Path to a one-column, whitespace-separated RUL label file.

    Returns:
        A numeric Series named ``RUL``.

    Raises:
        FileNotFoundError: If ``file_path`` does not exist.
        ValueError: If the path is not a file, the file is empty, cannot be
            parsed as numeric data, or does not contain exactly one column.
    """
    path = _validate_file_path(file_path, "C-MAPSS RUL target")

    try:
        targets = pd.read_csv(path, sep=r"\s+", header=None)
    except pd.errors.EmptyDataError as error:
        raise ValueError(f"C-MAPSS RUL target file is empty: {path}") from error
    except (OSError, pd.errors.ParserError) as error:
        raise ValueError(f"Unable to parse C-MAPSS RUL target file: {path}") from error

    if targets.empty:
        raise ValueError(f"C-MAPSS RUL target file is empty: {path}")

    if targets.shape[1] != 1:
        raise ValueError(
            f"Malformed C-MAPSS RUL target file {path}: expected 1 column, "
            f"found {targets.shape[1]}."
        )

    try:
        return pd.to_numeric(targets.iloc[:, 0], errors="raise").rename(RUL_COLUMN)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"Malformed C-MAPSS RUL target file {path}: all values must be numeric."
        ) from error
