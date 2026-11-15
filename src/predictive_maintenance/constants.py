"""Shared schema definitions for the NASA C-MAPSS FD001 project."""

ENGINE_ID_COLUMN = "engine_id"
CYCLE_COLUMN = "cycle"
MAX_CYCLE_COLUMN = "max_cycle"
RUL_COLUMN = "RUL"

RAW_COLUMN_NAMES = (
    ENGINE_ID_COLUMN,
    CYCLE_COLUMN,
    *(f"setting_{index}" for index in range(1, 4)),
    *(f"sensor_{index}" for index in range(1, 22)),
)

CONSTANT_FEATURES = (
    "setting_3",
    "sensor_1",
    "sensor_5",
    "sensor_10",
    "sensor_16",
    "sensor_18",
    "sensor_19",
)

MODEL_FEATURES = (
    "setting_1",
    "setting_2",
    "sensor_2",
    "sensor_3",
    "sensor_4",
    "sensor_6",
    "sensor_7",
    "sensor_8",
    "sensor_9",
    "sensor_11",
    "sensor_12",
    "sensor_13",
    "sensor_14",
    "sensor_15",
    "sensor_17",
    "sensor_20",
    "sensor_21",
)
