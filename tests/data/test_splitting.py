"""Tests for engine-aware data splitting."""

from predictive_maintenance.data.splitting import split_by_engine


def test_split_by_engine_keeps_engine_trajectories_disjoint(cmapss_trajectory):
    """No engine may appear in both the training and validation subsets."""
    train_data, validation_data = split_by_engine(
        cmapss_trajectory,
        validation_size=1 / 3,
        random_state=42,
    )

    train_engines = set(train_data["engine_id"])
    validation_engines = set(validation_data["engine_id"])

    assert train_engines
    assert validation_engines
    assert train_engines.isdisjoint(validation_engines)
    assert train_engines | validation_engines == {1, 2, 3}
