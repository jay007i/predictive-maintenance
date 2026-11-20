"""Tests for C-MAPSS trajectory validation."""

import pytest

from predictive_maintenance.data.validation import validate_cmapss_trajectory


def test_validate_cmapss_trajectory_accepts_valid_data(cmapss_trajectory):
    """A complete, unique trajectory passes validation."""
    validate_cmapss_trajectory(cmapss_trajectory)


def test_validate_cmapss_trajectory_rejects_duplicate_engine_cycle(cmapss_trajectory):
    """Duplicate records are rejected because they make trajectory state ambiguous."""
    duplicate_data = cmapss_trajectory.iloc[[0]].copy()
    invalid_data = cmapss_trajectory.copy()
    invalid_data.loc[len(invalid_data)] = duplicate_data.iloc[0]

    with pytest.raises(ValueError, match="duplicate engine-cycle"):
        validate_cmapss_trajectory(invalid_data)


def test_validate_cmapss_trajectory_rejects_missing_raw_column(cmapss_trajectory):
    """Missing schema columns fail before preprocessing or inference."""
    invalid_data = cmapss_trajectory.drop(columns="sensor_21")

    with pytest.raises(ValueError, match="sensor_21"):
        validate_cmapss_trajectory(invalid_data)
