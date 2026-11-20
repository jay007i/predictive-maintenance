"""Tests for shared training and inference preprocessing."""

from predictive_maintenance.constants import MODEL_FEATURES, RUL_COLUMN
from predictive_maintenance.data.preprocessing import (
    add_rul_target,
    prepare_inference_data,
    prepare_training_data,
    select_final_engine_cycles,
)


def test_add_rul_target_does_not_mutate_input(cmapss_trajectory):
    """RUL engineering returns a new DataFrame with expected target values."""
    labeled_data = add_rul_target(cmapss_trajectory)

    assert RUL_COLUMN not in cmapss_trajectory.columns
    assert labeled_data.groupby("engine_id")[RUL_COLUMN].min().eq(0).all()
    assert labeled_data.groupby("engine_id")[RUL_COLUMN].max().eq(2).all()


def test_prepare_training_data_preserves_model_feature_order(cmapss_trajectory):
    """Training features follow the saved model's exact contract."""
    features, target = prepare_training_data(add_rul_target(cmapss_trajectory))

    assert tuple(features.columns) == MODEL_FEATURES
    assert target.name == RUL_COLUMN
    assert features.shape == (9, 17)


def test_prepare_inference_data_keeps_only_final_engine_cycles(cmapss_trajectory):
    """Inference returns one ordered feature row per engine."""
    final_cycles = select_final_engine_cycles(cmapss_trajectory)
    features = prepare_inference_data(cmapss_trajectory)

    assert final_cycles["cycle"].tolist() == [3, 3, 3]
    assert tuple(features.columns) == MODEL_FEATURES
    assert features.shape == (3, 17)
