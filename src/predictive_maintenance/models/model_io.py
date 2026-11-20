"""Functions for loading and validating serialized model artifacts."""

from pathlib import Path
from typing import Any

import joblib

from predictive_maintenance.constants import MODEL_FEATURES


def load_model(file_path: str | Path) -> Any:
    """Load a serialized model artifact from an explicit local path.

    Args:
        file_path: Path to a joblib model artifact.

    Returns:
        The deserialized model object.

    Raises:
        FileNotFoundError: If ``file_path`` does not exist.
        ValueError: If the path is not a file or cannot be deserialized.

    Warning:
        Joblib artifacts are pickle-based. Only load artifacts from trusted
        sources because deserializing untrusted files can execute code.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Model artifact not found: {path}")

    if not path.is_file():
        raise ValueError(f"Model artifact path is not a file: {path}")

    try:
        return joblib.load(path)
    except (EOFError, ImportError, OSError, ValueError) as error:
        raise ValueError(f"Unable to load model artifact: {path}") from error


def validate_model_feature_contract(model: Any) -> None:
    """Validate that a model is compatible with the 17-feature FD001 contract.

    Args:
        model: A fitted estimator or pipeline exposing ``predict``.

    Raises:
        TypeError: If the object does not expose a prediction method.
        ValueError: If known model metadata conflicts with ``MODEL_FEATURES``.
    """
    if not callable(getattr(model, "predict", None)):
        raise TypeError("Model must expose a callable predict method.")

    expected_feature_count = len(MODEL_FEATURES)
    model_feature_count = getattr(model, "n_features_in_", None)
    if model_feature_count is not None and model_feature_count != expected_feature_count:
        raise ValueError(
            "Model feature contract mismatch: expected "
            f"{expected_feature_count} features, found {model_feature_count}."
        )

    model_feature_names = getattr(model, "feature_names_in_", None)
    if model_feature_names is not None and tuple(model_feature_names) != MODEL_FEATURES:
        raise ValueError(
            "Model feature contract mismatch: feature names do not match "
            "the required MODEL_FEATURES order."
        )
