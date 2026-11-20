"""Shared synthetic fixtures for predictive-maintenance tests."""

import pandas as pd
import pytest

from predictive_maintenance.constants import RAW_COLUMN_NAMES


@pytest.fixture
def cmapss_trajectory() -> pd.DataFrame:
    """Return a small valid trajectory with three engines and three cycles."""
    rows = []
    for engine_id in (1, 2, 3):
        for cycle in (1, 2, 3):
            row = {column: float(index) for index, column in enumerate(RAW_COLUMN_NAMES)}
            row["engine_id"] = engine_id
            row["cycle"] = cycle
            rows.append(row)

    return pd.DataFrame(rows, columns=RAW_COLUMN_NAMES)
