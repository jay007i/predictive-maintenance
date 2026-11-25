# Predictive Maintenance: NASA C-MAPSS FD001

This project estimates remaining useful life (RUL) from the simulated NASA
C-MAPSS aircraft-engine degradation dataset. It is a portfolio learning project,
not a deployed production system or evidence of real-world business impact.

## Selected model

The completed notebook experiments selected the tuned Support Vector Regressor
stored at `artifacts/models/svr_tuned.joblib`. It is a scikit-learn pipeline:

```text
StandardScaler -> SVR(C=50, epsilon=1, gamma=0.01)
```

The model requires the exact ordered 17-column contract in
`predictive_maintenance.constants.MODEL_FEATURES`. Scaling remains inside the
saved model pipeline; callers must not scale features separately.

## Reusable package

```text
src/predictive_maintenance/
├── constants.py             # Dataset and model-feature contracts
├── inference.py             # Engine-aligned RUL prediction orchestration
├── data/
│   ├── loaders.py           # C-MAPSS trajectories and official RUL labels
│   ├── preprocessing.py     # RUL target and feature preparation
│   ├── splitting.py         # Leakage-safe engine-level split
│   └── validation.py        # Trajectory integrity checks
└── models/
    ├── evaluation.py        # MAE, RMSE, and R-squared
    └── model_io.py          # Trusted local artifact loading and contract checks
```

Inference flow:

```text
raw C-MAPSS trajectory -> validate -> latest row per engine
-> ordered 17 features -> saved SVR pipeline -> engine_id + predicted_rul
```

## Data versioning — DVC and Amazon S3

The project uses DVC to track the three NASA C-MAPSS FD001 datasets:

- `train_FD001.txt`
- `test_FD001.txt`
- `RUL_FD001.txt`

### Architecture

- Git tracks DVC metadata (`.dvc` files) and shared project configuration.
- DVC stores dataset contents in its local cache.
- Amazon S3 acts as the remote storage for versioned dataset contents.
- AWS CLI authentication is configured locally using temporary credentials.
- Machine-specific AWS configuration is excluded from Git.

### Reproducing the data environment

Install project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Authenticate with your configured AWS profile, then restore the datasets:

```powershell
dvc pull
```

Check data synchronization:

```powershell
dvc status -c
```

Upload updated tracked data:

```powershell
dvc push
```

### Verification

- Three FD001 datasets successfully uploaded to Amazon S3.
- DVC reports local cache and remote storage in sync.
- A fresh Git clone successfully restored all three datasets using `dvc pull`.

## Installation and verification

From the project root, install the pinned dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The suite uses synthetic fixtures for unit tests and, when local FD001 data and
the saved tuned SVR artifact are available, verifies the official test-set
result. The Stage 5 verification reproduced MAE `19.45082771133248`, RMSE
`27.280498923453568`, and R-squared `0.5690319515077737`.

## Current scope and limitations

- The package supports the completed FD001 feature contract only.
- RUL target generation is valid only for run-to-failure training trajectories.
- Official test trajectories are reduced to their final observed cycle.
- Joblib artifacts are pickle-based: load only trusted local artifacts.
- DVC data versioning and Amazon S3 remote storage are implemented
  for the three FD001 datasets.
- DVC pipeline orchestration is not yet implemented.
- MLflow, FastAPI, Docker, CI/CD, deployment, and monitoring
  are planned for subsequent project stages.
