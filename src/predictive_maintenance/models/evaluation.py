"""Regression evaluation functions for RUL predictions."""

from collections.abc import Sequence

from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error


def evaluate_regression(
    y_true: Sequence[float], y_predicted: Sequence[float]
) -> dict[str, float]:
    """Calculate standard regression metrics for remaining-useful-life values.

    Args:
        y_true: Observed RUL values.
        y_predicted: Predicted RUL values in the same order as ``y_true``.

    Returns:
        A dictionary containing mean absolute error, root mean squared error,
        and R-squared under the keys ``mae``, ``rmse``, and ``r2``.

    Raises:
        ValueError: If inputs are empty, have different lengths, or cannot be
            evaluated by scikit-learn.
    """
    if len(y_true) == 0:
        raise ValueError("Regression targets must not be empty.")

    if len(y_true) != len(y_predicted):
        raise ValueError("Regression targets and predictions must have equal length.")

    return {
        "mae": float(mean_absolute_error(y_true, y_predicted)),
        "rmse": float(root_mean_squared_error(y_true, y_predicted)),
        "r2": float(r2_score(y_true, y_predicted)),
    }
