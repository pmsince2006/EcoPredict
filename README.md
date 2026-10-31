# EcoPredict — AI-Powered Air Quality Intelligence & Forecasting Platform

[![Checkpoint](https://img.shields.io/badge/Hackathon-Checkpoint%202%3A%20Data%20%26%20Baseline%20ML-success.svg)](#current-project-status-and-roadmap)
[![Frontend](https://img.shields.io/badge/Frontend-React%2018%20%2B%20TypeScript%20%2B%20Vite-61dafb.svg)](#proposed-technology-stack)
[![Backend](https://img.shields.io/badge/Backend-FastAPI%20%2B%20Python%203.12-009688.svg)](#proposed-technology-stack)
[![ML-Pipeline](https://img.shields.io/badge/ML--Pipeline-scikit--learn%20%2B%20pandas-f7931e.svg)](#machine-learning-workflow)
[![License](https://img.shields.io/badge/License-MIT%20(Proposed)-yellow.svg)](#license)

> **EcoPredict** is an ambient environmental intelligence platform engineered to monitor micro-climatic air pollution, forecast multi-horizon Air Quality Index (AQI) dynamics using machine learning, and empower citizens with clean-route transit planning to minimize toxic particulate exposure.

---

## 1. Project Title & Description

**EcoPredict** is an end-to-end environmental intelligence application designed to address urban air pollution crises in severely affected regions (such as the National Capital Region of Delhi and major metropolitan basins). The platform aggregates multi-sensor ambient particulate telemetry ($PM_{2.5}, PM_{10}, NO_2, SO_2, CO, O_3$), applies time-series and meteorological feature engineering, forecasts forward-looking AQI trends, and delivers proactive health recommendations and clean routing guidance.

> [!IMPORTANT]
> **Hackathon Checkpoint 2 Update**: This repository contains **Checkpoint 2: Dataset Validation and Baseline AQI Forecasting**. We have implemented and tested a complete, reproducible machine-learning pipeline:
> - **Data Provenance & Quality**: Documented candidate sources (CPCB, OpenAQ v3, data.gov.in) and quality findings in [`docs/dataset.md`](docs/dataset.md).
> - **Modeling & AQI Standard**: Formulated continuous $PM_{2.5}$ forecasting vs CPCB sub-index formulas in [`docs/modeling.md`](docs/modeling.md).
> - **Data Pipeline**: Implemented schema validation, timestamp parsing, deduplication, and anomaly sanitization in [`ml/src/data/loader.py`](ml/src/data/loader.py).
> - **Feature Engineering**: Implemented autoregressive lags, trailing rolling statistics, and cyclical time encodings with strict zero-leakage guarantees in [`ml/src/features/engineer.py`](ml/src/features/engineer.py).
> - **Baseline Modeling**: Implemented chronological train/val/test splitting, a persistence baseline, and a Random Forest regressor with side-by-side evaluation in [`ml/src/training/train.py`](ml/src/training/train.py) and [`ml/src/evaluation/evaluate.py`](ml/src/evaluation/evaluate.py).
> - **Reproducible Tests**: Added comprehensive test coverage in [`tests/ml/`](tests/ml/) using a validated software test fixture (`ml/data/raw/sample_delhi_cpcb_fixture.csv`).

---

## 2. Problem Statement & Motivation

Urban air pollution is among the most severe environmental health hazards of the modern era:
- **Severe Particulate Infiltration**: Fine particulate matter ($PM_{2.5}$) penetrates deep into lung tissue and enters the bloodstream, contributing to chronic respiratory conditions, cardiovascular mortality, and reduced life expectancy.
- **Diurnal Volatility & Temperature Inversions**: Stagnant meteorological conditions, agricultural biomass burning, and vehicular exhaust create sudden localized pollution spikes that traditional retrospective reporting fails to anticipate.
- **Lagging Retrospective Reporting**: Most existing civic monitoring portals only report historical or delayed readings (e.g. past 24-hour averages), leaving citizens unable to plan their outdoor commutes or exercise around impending hazardous peaks.
- **Actionability Gap**: Current dashboards report abstract numbers without translating them into actionable, preventative decisions such as identifying the cleanest transit corridor or advising vulnerable individuals when to stay indoors.

*Source Assumption Note: As the official hackathon problem statement was not bundled directly in the repository root, EcoPredict is specified herein as an AI-driven ambient air monitoring and forecasting platform.*

---

## 3. Proposed Solution

EcoPredict bridges the gap between raw environmental sensors and civic decision-making through a three-tier system:

1. **Continuous Telemetry & Data Validation**: Systematic ingestion of station-level air quality and weather telemetry, coupled with anomaly detection and automated sensor dropout imputation.
2. **Machine-Learning Forecasting Engine**: Supervised regression and time-series models trained on lagged particulate concentrations and cyclical meteorological patterns to predict $+1\text{h}$, $+6\text{h}$, and $+24\text{h}$ AQI trajectories.
3. **Action-Oriented Decision Dashboard**: A responsive, dark-slate user dashboard featuring real-time severity badges, interactive geospatial hotspot maps, confidence-bounded forecast curves, and an experimental clean-route exposure planner.

---

## 4. Target Users & Use Cases

| Target User Group | Core Needs | Primary Platform Use Case |
| :--- | :--- | :--- |
| **Vulnerable Citizens** *(Asthmatics, Elderly, Children)* | Timely notification of hazardous particulate spikes | Receive proactive advisories to wear N95 protection or avoid outdoor activities during predicted inversions. |
| **Daily Commuters & Cyclists** | Routes with minimum toxic exposure | Compare transit alternatives and select routes that circumvent high-emission industrial corridors. |
| **Municipal & Environmental Planners** | Spatial pollution attribution and hotspot tracking | Monitor localized anomalies and identify primary source contributions (traffic, industry, dust, biomass). |
| **Healthcare Providers & Researchers** | Granular multi-pollutant telemetry trends | Correlate respiratory admission spikes with forward-looking air quality forecasts. |

---

## 5. Project Roadmap & Implemented Features

### Checkpoint 1: Foundation (Completed)
- [x] Comprehensive repository structure and environment configuration templates.
- [x] Proposed system architecture and data-flow documentation.
- [x] Interactive React + TypeScript + Vite frontend dashboard shell with dark-slate UI.
- [x] Modular UI components based on environmental intelligence design references.
- [x] Representative demonstration telemetry data and simulated forecast curves.
- [x] FastAPI backend scaffold with health endpoints, CORS middleware, and Pydantic schemas.

### Checkpoint 2: Dataset Validation & Baseline ML (Completed)
- [x] Investigated candidate data sources (CPCB CCR portal, OpenAQ v3 API, data.gov.in) and verified access requirements.
- [x] Documented data provenance, sampling conventions, missingness, and retrieval steps in [`docs/dataset.md`](docs/dataset.md).
- [x] Formulated prediction task, CPCB NAQI sub-index formulas vs raw concentration, and leakage safeguards in [`docs/modeling.md`](docs/modeling.md).
- [x] Implemented robust CSV data ingestion with schema validation, duplicate deduplication, and anomaly handling in [`ml/src/data/loader.py`](ml/src/data/loader.py).
- [x] Implemented zero-leakage feature engineering (lags, velocity, trailing rolling means, cyclical encodings) in [`ml/src/features/engineer.py`](ml/src/features/engineer.py).
- [x] Implemented strict chronological splitting, persistence baseline, and Random Forest regression in [`ml/src/training/train.py`](ml/src/training/train.py).
- [x] Implemented regression benchmarking (MAE, RMSE, $R^2$, MAPE) with side-by-side baseline comparison in [`ml/src/evaluation/evaluate.py`](ml/src/evaluation/evaluate.py).
- [x] Implemented model and metadata serialization (`ml/models/`).
- [x] Provided validated software test fixture (`ml/data/raw/sample_delhi_cpcb_fixture.csv`) and comprehensive unit tests in [`tests/ml/`](tests/ml/).

### Checkpoint 3: Live Integration & Route Optimization (Upcoming)
- [ ] Connect FastAPI prediction endpoints to loaded model artifacts.
- [ ] Ingest production multi-month CPCB / OpenAQ historical datasets.
- [ ] Graph-based clean route optimization across transit corridors.
- [ ] Automated model retraining and evaluation dashboard integration.

---

## 6. Technology Stack

| Domain | Technology | Justification / Reason |
| :--- | :--- | :--- |
| **Frontend Framework** | **React 18 + TypeScript** | Strong type safety, reusable component lifecycle, and rich ecosystem for scientific interfaces. |
| **Build Tool** | **Vite 5** | Lightning-fast Hot Module Replacement (HMR) and optimized ES module bundling. |
| **Styling** | **Tailwind CSS** | Utility-first CSS allowing data-dense, dark charcoal layouts with consistent spacing. |
| **Visual Charts** | **Recharts** | Declarative React charting library for confidence-interval forecast curves and historical trends. |
| **Geospatial Maps** | **Leaflet** | Lightweight, responsive mapping library with custom tile overlays and hotspot markers. |
| **Backend API** | **FastAPI (Python 3.12)** | Asynchronous high-performance REST framework with automatic OpenAPI documentation and strict Pydantic typing. |
| **Data Processing** | **pandas & NumPy** | Industry-standard tabular data manipulation, time-series resampling, and array computation. |
| **Machine Learning** | **scikit-learn** | Robust collection of regression algorithms, cross-validation utilities, and feature transformers. |
| **Testing** | **pytest** | Concise, scalable unit and smoke testing for Python backend and ML pipeline code. |

---

## 7. High-Level Architecture

```mermaid
flowchart LR
    A["Raw Data Sources\n(CPCB, OpenAQ, Weather)"] --> B["Data Validation & Imputation\n(ml/src/data/loader.py)"]
    B --> C["Feature Engineering\n(Lags, Diurnal, Trailing Means)"]
    C --> D["Model Training & Evaluation\n(Persistence vs Random Forest)"]
    D --> E["Saved Model Artifact\n(ml/models/*.pkl, metadata.json)"]
    E --> F["FastAPI Prediction API\n(backend/app/main.py)"]
    F --> G["React Dashboard\n(frontend/src/)"]
    G --> H["Actionable Insights\n(Forecasts, Alerts, Route Planner)"]
```

---

## 8. Project Folder Structure

```
EcoPredict/
├── README.md                      # Comprehensive project overview and setup guide
├── .gitignore                     # Multi-environment ignore file (Python, Node, ML artifacts)
├── .env.example                   # Environment variable template with safe placeholders
├── LICENSE                        # MIT License
├── docs/
│   ├── architecture.md            # Detailed system architecture and interface specification
│   ├── ui-design.md               # UI design system, color tokens, and layout guidelines
│   ├── dataset.md                 # Dataset provenance, CPCB/OpenAQ access, quality findings
│   └── modeling.md                # Forecasting formulation, NAQI calculations, leakage rules
├── frontend/                      # React + TypeScript + Vite web client
│   ├── src/
│   │   ├── components/            # Reusable UI primitives (Header, Badges)
│   │   ├── features/dashboard/    # Dashboard cards, Leaflet map, forecast & trend charts
│   │   ├── layouts/               # Page wrapper layouts
│   │   ├── pages/                 # Top-level routed pages
│   │   ├── services/              # API clients and mock telemetry fixtures
│   │   ├── types/                 # Shared TypeScript interfaces (AQI, Stations, Forecasts)
│   │   └── utils/                 # Severity calculators and formatting utilities
│   ├── package.json               # Frontend dependencies and run scripts
│   └── vite.config.ts             # Vite build and dev-server configuration
├── backend/                       # FastAPI REST microservice
│   ├── app/
│   │   ├── api/routes/            # Route modules (health, aqi endpoints)
│   │   ├── core/                  # Application configuration and settings
│   │   ├── schemas/               # Pydantic data contracts and models
│   │   ├── services/              # Business logic and mock service layers
│   │   └── main.py                # FastAPI application initialization and CORS setup
│   └── requirements.txt           # Python backend dependencies
├── ml/                            # Machine Learning & Data Science pipeline
│   ├── data/
│   │   ├── raw/                   # Raw sensor datasets & sample_delhi_cpcb_fixture.csv
│   │   └── processed/             # Cleaned feature-engineered datasets
│   ├── notebooks/                 # Exploratory data analysis (EDA) notebooks
│   ├── src/                       # Production ML pipeline code
│   │   ├── data/loader.py         # CSV loading, schema validation, anomaly sanitization
│   │   ├── features/engineer.py   # Lags, rate-of-change, trailing rolling means, cyclical time
│   │   ├── training/train.py      # Chronological split, persistence baseline, Random Forest
│   │   └── evaluation/evaluate.py # MAE, RMSE, R2, MAPE, baseline comparison reports
│   ├── models/                    # Serialized model weights & model_metadata.json
│   ├── reports/                   # Model performance evaluation artifacts
│   └── requirements.txt           # Python data science dependencies
└── tests/                         # Unit and smoke test suites
    ├── backend/                   # FastAPI endpoint and service tests
    └── ml/                        # ML pipeline tests (loader, feature engineer, trainer)
```

---

## 9. Setup & Installation Instructions

### Prerequisites
- **Node.js**: Version `18.0.0` or higher (`v24.x` verified)
- **Python**: Version `3.10` to `3.12` (`Python 3.12.5` verified)
- **Git**

---

### Step A: Clone the Repository
```bash
git clone https://github.com/pmsince2006/EcoPredict.git
cd EcoPredict
```

---

### Step B: Frontend Setup
1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. Open your browser and navigate to `http://localhost:5173`.
3. To run a production type-check and build:
   ```bash
   npm run build
   ```

---

### Step C: Machine Learning Pipeline & Training
1. Navigate to the `ml/` directory:
   ```bash
   cd ml
   pip install -r requirements.txt
   ```
2. Run the complete training and evaluation pipeline on the verified test fixture:
   ```bash
   python -m src.training.train
   ```
   *This command loads the dataset, validates columns, constructs features, performs chronological splitting, fits both persistence and Random Forest models, compares metrics side-by-side, and serializes artifacts to `ml/models/`.*

---

### Step D: Backend Setup
1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
2. View interactive API documentation at `http://127.0.0.1:8000/docs`.

---

## 10. Environment Variables & Configuration

A configuration template is provided in `.env.example`. Copy this template to create your local `.env` file:

```bash
cp .env.example .env
```

| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `ENVIRONMENT` | `development` | Deployment environment (`development`, `staging`, `production`) |
| `DEBUG` | `True` | Enables verbose error messages and tracebacks |
| `BACKEND_HOST` | `127.0.0.1` | Local listening host for FastAPI server |
| `BACKEND_PORT` | `8000` | Port for FastAPI service |
| `VITE_API_BASE_URL` | `http://localhost:8000/api` | API root consumed by frontend services |
| `VITE_ENABLE_MOCK_DATA` | `true` | Allows frontend to fall back to simulated telemetry data |
| `OPENAQ_API_KEY` | *(Placeholder)* | API key for external OpenAQ data ingestion (Checkpoint 2/3) |
| `OPENWEATHER_API_KEY` | *(Placeholder)* | API key for ambient weather telemetry (Checkpoint 2/3) |
| `MODEL_ARTIFACTS_DIR` | `ml/models` | Local directory for storing serialized model weights |

---

## 11. Machine-Learning Workflow

```
[ Raw CSV Dataset ]
         │
         ▼
[ ml/src/data/loader.py: DataLoader.load_dataset() ]
  - Validates required columns (timestamp, station_id, pm25)
  - Parses timestamps to datetime64
  - Deduplicates timestamp records
  - Sanitizes negative sensor readings to NaN
         │
         ▼
[ ml/src/features/engineer.py: FeatureEngineer.create_features() ]
  - Auto-regressive lags: y_{t-1}, y_{t-2}, y_{t-3}, y_{t-6}, y_{t-12}, y_{t-24}
  - Velocity delta: y_t - y_{t-1}
  - Trailing rolling statistics (strictly backward, NO centered windows)
  - Diurnal cyclical encodings: sin/cos(2*pi*hour/24)
  - Target creation: y_{t + horizon}
         │
         ▼
[ ml/src/training/train.py: chronological_split() ]
  - Train (70%) ──▶ Validation (15%) ──▶ Test (15%)
  - No random shuffling; chronological evaluation
         │
         ├──▶ Persistence Baseline: y_hat = y_t
         └──▶ Random Forest Regressor: fitted strictly on X_train
         │
         ▼
[ ml/src/evaluation/evaluate.py: ModelEvaluator ]
  - Computes MAE, RMSE, R2, MAPE on held-out test data
  - Computes relative improvement percentage over persistence
         │
         ▼
[ ml/models/ ]
  - Serialized model weights (baseline_random_forest.pkl)
  - Training metadata & evaluation report (model_metadata.json)
```

---

## 12. Testing Instructions

### Run ML Test Suite
Run pytest from the repository root:
```bash
pytest tests/ml/ -v
```

The test suite validates:
1. `test_load_valid_csv`: Valid schema and datetime parsing.
2. `test_missing_file_raises_not_found`: `FileNotFoundError` handling.
3. `test_missing_required_columns`: `DataValidationError` when columns are absent.
4. `test_invalid_timestamp_raises_error`: Unparseable date strings rejected.
5. `test_duplicate_records_deduplication`: Duplicate timestamps detected and deduplicated.
6. `test_negative_readings_sanitized`: Negative sensor artifacts sanitized to `NaN` without row loss.
7. `test_feature_engineer_dimensions`: Feature matrix shapes and expected column names.
8. `test_target_horizon_alignment`: Target shift alignment verification ($y_t = x_{t+h}$).
9. `test_absence_of_future_data_leakage`: Proves modifying future data ($t+1, \dots$) leaves features at time $t$ identical.
10. `test_chronological_split_ordering`: Proves strict chronological partition without index overlap.
11. `test_evaluator_known_metrics`: Analytical metric calculation verification (MAE, RMSE).
12. `test_trainer_end_to_end_on_fixture`: Full end-to-end pipeline execution on software test fixture.

### Run Backend Smoke Tests
```bash
python -c "
import tests.backend.test_health as tb
tb.test_settings_initialization()
tb.test_aqi_service_severity_categories()
tb.test_aqi_demo_summary()
print('✓ Backend tests passed!')
"
```

### Run Frontend Build Test
```bash
cd frontend
npm run build
```

---

## 13. Team Contributions

| Team Member | Role Focus | Checkpoint 2 Responsibilities |
| :--- | :--- | :--- |
| **Member 1 (Prince)** | **Fullstack Lead & Coordination** | Repository architecture, interface alignment, and pipeline reproducibility. |
| **Member 2** | **Frontend & UI/UX Developer** | Maintained UI shell integrity, reviewed data contracts for Checkpoint 3 integration. |
| **Member 3** | **Data Engineer & Pipeline Lead** | Implemented `DataLoader`, investigated CPCB/OpenAQ sources, authored `docs/dataset.md`. |
| **Member 4** | **Machine Learning Specialist** | Implemented `FeatureEngineer`, `ModelTrainer`, `ModelEvaluator`, authored `docs/modeling.md`. |

---

## 14. License

This project is developed as part of a hackathon submission under the **MIT License** — see [LICENSE](LICENSE) for details.
