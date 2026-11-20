"""Read-only integration verification against the saved FD001 SVR artifact."""

from pathlib import Path

import pytest

from predictive_maintenance.constants import PREDICTED_RUL_COLUMN
from predictive_maintenance.data.loaders import load_cmapss_data, load_rul_targets
from predictive_maintenance.inference import predict_rul
from predictive_maintenance.models.evaluation import evaluate_regression
from predictive_maintenance.models.model_io import load_model


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "test_FD001.txt"
TARGET_PATH = PROJECT_ROOT / "data" / "raw" / "RUL_FD001.txt"
MODEL_PATH = PROJECT_ROOT / "artifacts" / "models" / "svr_tuned.joblib"


@pytest.mark.integration
def test_saved_tuned_svr_reproduces_fd001_evaluation():
    """The architecture reproduces the notebook's saved-model FD001 metrics."""
    required_paths = (TEST_DATA_PATH, TARGET_PATH, MODEL_PATH)
    if not all(path.exists() for path in required_paths):
        pytest.skip("FD001 data or saved tuned SVR artifact is unavailable.")

    predictions = predict_rul(
        load_cmapss_data(TEST_DATA_PATH),
        load_model(MODEL_PATH),
    )
    metrics = evaluate_regression(
        load_rul_targets(TARGET_PATH),
        predictions[PREDICTED_RUL_COLUMN],
    )

    assert predictions.shape == (100, 2)
    assert metrics["mae"] == pytest.approx(19.45082771133248)
    assert metrics["rmse"] == pytest.approx(27.280498923453568)
    assert metrics["r2"] == pytest.approx(0.5690319515077737)
