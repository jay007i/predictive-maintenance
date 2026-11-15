"""Preprocessing functions shared by C-MAPSS training and inference workflows."""

import pandas as pd

from predictive_maintenance.constants import (
    CYCLE_COLUMN,
    ENGINE_ID_COLUMN,
    MODEL_FEATURES,
    RUL_COLUMN,
)


def _validate_required_columns(
    data: pd.DataFrame, required_columns: tuple[str, ...], data_name: str
) -> None:
    """Raise an error when a DataFrame is missing required columns."""
    missing_columns = sorted(set(required_columns) - set(data.columns))
    if missing_columns:
        raise ValueError(
            f"{data_name} is missing required columns: {', '.join(missing_columns)}."
        )


def add_rul_target(data: pd.DataFrame) -> pd.DataFrame:
    """Create the row-level remaining useful life target for training data.

    RUL is the difference between an engine's final observed training cycle and
    its current cycle. This function is intended only for run-to-failure
    training trajectories, where the final cycle represents failure.

    Args:
        data: C-MAPSS training data containing engine and cycle columns.

    Returns:
        A copy of ``data`` with an ``RUL`` column.

    Raises:
        ValueError: If the engine identifier or cycle column is missing.
    """
    _validate_required_columns(
        data,
        (ENGINE_ID_COLUMN, CYCLE_COLUMN),
        "Training data",
    )

    processed_data = data.copy()
    max_cycles = processed_data.groupby(ENGINE_ID_COLUMN)[CYCLE_COLUMN].transform("max")
    processed_data[RUL_COLUMN] = max_cycles - processed_data[CYCLE_COLUMN]
    return processed_data


def prepare_training_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Separate ordered model features and the RUL target for training.

    Args:
        data: Training data that already contains the row-level ``RUL`` target.

    Returns:
        A tuple of the 17-column feature DataFrame and the RUL target Series.

    Raises:
        ValueError: If a required model feature or the RUL target is missing.
    """
    _validate_required_columns(
        data,
        (*MODEL_FEATURES, RUL_COLUMN),
        "Training data",
    )

    features = data.loc[:, list(MODEL_FEATURES)].copy()
    target = data[RUL_COLUMN].copy()
    return features, target


def prepare_inference_data(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare final-cycle, ordered model features for C-MAPSS inference.

    The official C-MAPSS test set contains a trajectory for each engine. This
    function retains each engine's latest observed cycle before selecting only
    the model features, so identifier and target columns cannot enter the
    saved model pipeline.

    Args:
        data: C-MAPSS trajectory data containing one or more engine cycles.

    Returns:
        A 17-column feature DataFrame with one row per engine, ordered by engine
        identifier and with columns in ``MODEL_FEATURES`` order.

    Raises:
        ValueError: If required identifiers or model features are missing.
    """
    _validate_required_columns(
        data,
        (ENGINE_ID_COLUMN, CYCLE_COLUMN, *MODEL_FEATURES),
        "Inference data",
    )

    latest_cycles = (
        data.sort_values([ENGINE_ID_COLUMN, CYCLE_COLUMN])
        .groupby(ENGINE_ID_COLUMN, sort=False)
        .tail(1)
        .sort_values(ENGINE_ID_COLUMN)
    )
    return latest_cycles.loc[:, list(MODEL_FEATURES)].copy()
