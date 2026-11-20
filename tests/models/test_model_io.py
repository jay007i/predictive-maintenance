"""Tests for serialized model loading and feature-contract validation."""

import joblib
import pandas as pd
import pytest
from sklearn.dummy import DummyRegressor

from predictive_maintenance.constants import MODEL_FEATURES
from predictive_maintenance.models.model_io import (
    load_model,
    validate_model_feature_contract,
)


class FeatureMismatchModel:
    """Minimal fitted-model stand-in with an incompatible feature count."""

    n_features_in_ = 1

    def predict(self, features):
        """Return one placeholder prediction per row."""
        return [0.0] * len(features)


def test_load_model_and_validate_feature_contract(tmp_path):
    """A trusted 17-feature model can be loaded and validated."""
    features = pd.DataFrame([[0.0] * len(MODEL_FEATURES)], columns=MODEL_FEATURES)
    model = DummyRegressor(strategy="mean").fit(features, [1.0])
    path = tmp_path / "model.joblib"
    joblib.dump(model, path)

    loaded_model = load_model(path)

    validate_model_feature_contract(loaded_model)


def test_validate_model_feature_contract_rejects_incompatible_model():
    """Models trained on another feature shape cannot enter FD001 inference."""
    with pytest.raises(ValueError, match="expected 17 features"):
        validate_model_feature_contract(FeatureMismatchModel())
