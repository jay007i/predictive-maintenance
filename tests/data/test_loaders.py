"""Tests for C-MAPSS file loading."""

import pandas as pd
import pytest

from predictive_maintenance.constants import RAW_COLUMN_NAMES, RUL_COLUMN
from predictive_maintenance.data.loaders import load_cmapss_data, load_rul_targets


def test_load_cmapss_data_assigns_shared_schema(tmp_path, cmapss_trajectory):
    """A valid headerless trajectory receives the expected column names."""
    path = tmp_path / "trajectory.txt"
    cmapss_trajectory.to_csv(path, sep=" ", header=False, index=False)

    loaded_data = load_cmapss_data(path)

    assert loaded_data.shape == cmapss_trajectory.shape
    assert tuple(loaded_data.columns) == RAW_COLUMN_NAMES


def test_load_cmapss_data_rejects_missing_file(tmp_path):
    """A missing trajectory file produces a meaningful exception."""
    with pytest.raises(FileNotFoundError, match="not found"):
        load_cmapss_data(tmp_path / "missing.txt")


def test_load_rul_targets_returns_named_numeric_series(tmp_path):
    """Official RUL labels are loaded as a named numeric Series."""
    path = tmp_path / "rul.txt"
    pd.Series([10, 20, 30]).to_csv(path, header=False, index=False)

    targets = load_rul_targets(path)

    assert targets.name == RUL_COLUMN
    assert targets.tolist() == [10, 20, 30]


def test_load_rul_targets_rejects_multiple_columns(tmp_path):
    """RUL files must have exactly one column."""
    path = tmp_path / "invalid_rul.txt"
    path.write_text("1 2\n3 4\n", encoding="utf-8")

    with pytest.raises(ValueError, match="expected 1 column"):
        load_rul_targets(path)
