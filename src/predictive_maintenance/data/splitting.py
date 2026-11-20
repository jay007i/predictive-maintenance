"""Engine-aware data-splitting utilities for C-MAPSS experiments."""

import pandas as pd
from sklearn.model_selection import train_test_split

from predictive_maintenance.constants import ENGINE_ID_COLUMN
from predictive_maintenance.data.validation import validate_required_columns


def split_by_engine(
    data: pd.DataFrame,
    validation_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split C-MAPSS rows into disjoint train and validation engine groups.

    This reproduces the notebook's engine-level split strategy: all cycles for
    an engine belong entirely to either training or validation data.

    Args:
        data: Data containing an ``engine_id`` column.
        validation_size: Fraction of unique engines assigned to validation.
        random_state: Seed passed to scikit-learn's split function.

    Returns:
        Training and validation DataFrames, each copied from ``data``.

    Raises:
        ValueError: If engine identifiers are missing, fewer than two engines
            are present, or ``validation_size`` is outside the open interval
            from zero to one.
    """
    validate_required_columns(data, (ENGINE_ID_COLUMN,), "Split data")

    if not 0 < validation_size < 1:
        raise ValueError("validation_size must be greater than 0 and less than 1.")

    engine_ids = data[ENGINE_ID_COLUMN].unique()
    if len(engine_ids) < 2:
        raise ValueError("At least two unique engines are required for splitting.")

    train_engines, validation_engines = train_test_split(
        engine_ids,
        test_size=validation_size,
        random_state=random_state,
    )

    train_data = data.loc[data[ENGINE_ID_COLUMN].isin(train_engines)].copy()
    validation_data = data.loc[
        data[ENGINE_ID_COLUMN].isin(validation_engines)
    ].copy()
    return train_data, validation_data
