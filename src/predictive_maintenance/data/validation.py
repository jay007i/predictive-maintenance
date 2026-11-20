"""Validation functions for C-MAPSS trajectory data."""

from collections.abc import Iterable

import pandas as pd

from predictive_maintenance.constants import (
    CYCLE_COLUMN,
    ENGINE_ID_COLUMN,
    RAW_COLUMN_NAMES,
)


def validate_required_columns(
    data: pd.DataFrame,
    required_columns: Iterable[str],
    data_name: str,
) -> None:
    """Raise an error when a DataFrame does not contain required columns."""
    missing_columns = sorted(set(required_columns) - set(data.columns))
    if missing_columns:
        raise ValueError(
            f"{data_name} is missing required columns: {', '.join(missing_columns)}."
        )


def validate_cmapss_trajectory(data: pd.DataFrame) -> None:
    """Validate the structural integrity of a C-MAPSS trajectory DataFrame.

    The function allows additional columns such as ``RUL`` so it can validate
    both raw trajectories and training data after target engineering.

    Args:
        data: C-MAPSS data with the shared raw schema.

    Raises:
        ValueError: If required columns are missing, values are missing,
            engine or cycle values are not positive, or engine-cycle records
            are duplicated.
    """
    if data.empty:
        raise ValueError("C-MAPSS trajectory data is empty.")

    validate_required_columns(data, RAW_COLUMN_NAMES, "C-MAPSS trajectory data")

    raw_data = data.loc[:, list(RAW_COLUMN_NAMES)]
    if raw_data.isna().any().any():
        raise ValueError("C-MAPSS trajectory data contains missing raw values.")

    if (raw_data[ENGINE_ID_COLUMN] <= 0).any():
        raise ValueError("C-MAPSS engine identifiers must be positive.")

    if (raw_data[CYCLE_COLUMN] <= 0).any():
        raise ValueError("C-MAPSS cycle values must be positive.")

    if data.duplicated(subset=[ENGINE_ID_COLUMN, CYCLE_COLUMN]).any():
        raise ValueError(
            "C-MAPSS trajectory data contains duplicate engine-cycle records."
        )
