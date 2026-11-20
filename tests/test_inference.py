"""Tests for model inference orchestration."""

import pandas as pd
from sklearn.dummy import DummyRegressor

from predictive_maintenance.constants import MODEL_FEATURES, PREDICTED_RUL_COLUMN
from predictive_maintenance.inference import predict_rul


def test_predict_rul_returns_engine_aligned_predictions(cmapss_trajectory):
    """Inference returns one prediction for each final engine observation."""
    fit_features = pd.DataFrame([[0.0] * len(MODEL_FEATURES)], columns=MODEL_FEATURES)
    model = DummyRegressor(strategy="constant", constant=7.0).fit(fit_features, [7.0])

    predictions = predict_rul(cmapss_trajectory, model)

    assert predictions["engine_id"].tolist() == [1, 2, 3]
    assert predictions[PREDICTED_RUL_COLUMN].tolist() == [7.0, 7.0, 7.0]
