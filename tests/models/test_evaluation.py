"""Tests for regression metric calculation."""

import pytest

from predictive_maintenance.models.evaluation import evaluate_regression


def test_evaluate_regression_returns_expected_metrics():
    """Metric values match simple hand-checkable predictions."""
    metrics = evaluate_regression([1.0, 2.0, 3.0], [1.0, 2.0, 4.0])

    assert metrics["mae"] == pytest.approx(1 / 3)
    assert metrics["rmse"] == pytest.approx(1 / 3**0.5)
    assert metrics["r2"] == pytest.approx(0.5)


def test_evaluate_regression_rejects_mismatched_lengths():
    """Metrics require aligned targets and predictions."""
    with pytest.raises(ValueError, match="equal length"):
        evaluate_regression([1.0], [1.0, 2.0])
