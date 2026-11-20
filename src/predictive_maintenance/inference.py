"""Inference orchestration for the saved C-MAPSS RUL model."""

from typing import Any

import pandas as pd

from predictive_maintenance.constants import ENGINE_ID_COLUMN, PREDICTED_RUL_COLUMN
from predictive_maintenance.data.preprocessing import (
    select_final_engine_cycles,
    select_model_features,
)
from predictive_maintenance.data.validation import validate_cmapss_trajectory
from predictive_maintenance.models.model_io import validate_model_feature_contract


def predict_rul(data: pd.DataFrame, model: Any) -> pd.DataFrame:
    """Predict RUL from C-MAPSS trajectories using a fitted model pipeline.

    Args:
        data: Raw C-MAPSS trajectory data for one or more engines.
        model: A trusted fitted model compatible with ``MODEL_FEATURES``.

    Returns:
        A DataFrame with one row per engine and columns ``engine_id`` and
        ``predicted_rul``.

    Raises:
        ValueError: If trajectory data is invalid, the model contract does not
            match, or prediction fails.
        TypeError: If ``model`` does not expose a callable ``predict`` method.
    """
    validate_cmapss_trajectory(data)
    validate_model_feature_contract(model)

    final_cycles = select_final_engine_cycles(data)
    features = select_model_features(final_cycles)

    try:
        predictions = model.predict(features)
    except (TypeError, ValueError) as error:
        raise ValueError("Model prediction failed for the prepared C-MAPSS data.") from error

    if len(predictions) != len(final_cycles):
        raise ValueError("Model returned a prediction count that does not match engines.")

    prediction_frame = final_cycles.loc[:, [ENGINE_ID_COLUMN]].copy()
    prediction_frame[PREDICTED_RUL_COLUMN] = predictions
    return prediction_frame.reset_index(drop=True)
