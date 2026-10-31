# EcoPredict — AI-Powered Air Quality Intelligence & Forecasting Platform

[![Checkpoint](https://img.shields.io/badge/Hackathon-Checkpoint%201%3A%20Foundation-blue.svg)](#current-project-status-and-roadmap)
[![Frontend](https://img.shields.io/badge/Frontend-React%2018%20%2B%20TypeScript%20%2B%20Vite-61dafb.svg)](#proposed-technology-stack)
[![Backend](https://img.shields.io/badge/Backend-FastAPI%20%2B%20Python%203.12-009688.svg)](#proposed-technology-stack)
[![Styling](https://img.shields.io/badge/Styling-Tailwind%20CSS-38bdf8.svg)](#proposed-technology-stack)
[![License](https://img.shields.io/badge/License-MIT%20(Proposed)-yellow.svg)](#license)

> **EcoPredict** is an ambient environmental intelligence platform engineered to monitor micro-climatic air pollution, forecast multi-horizon Air Quality Index (AQI) dynamics using machine learning, and empower citizens with clean-route transit planning to minimize toxic particulate exposure.

---

## 1. Project Title & Description

**EcoPredict** is an end-to-end environmental intelligence application designed to address urban air pollution crises in severely affected regions (such as the National Capital Region of Delhi and major metropolitan basins). The platform aggregates multi-sensor ambient particulate telemetry ($PM_{2.5}, PM_{10}, NO_2, SO_2, CO, O_3$), applies time-series and meteorological feature engineering, forecasts forward-looking AQI trends, and delivers proactive health recommendations and clean routing guidance.

> [!IMPORTANT]
> **Hackathon Checkpoint 1 Note**: This repository currently houses the **Checkpoint 1: Project Foundation**. All project directory scaffolding, architectural contracts, backend/ML skeletons, and an interactive frontend dashboard shell with representative mock preview data are established. Real external data ingestion and trained machine-learning model binaries are planned for subsequent checkpoints.

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
2. **Machine-Learning Forecasting Engine**: Supervised regression and time-series models trained on lagged particulate concentrations and cyclical meteorological patterns to predict $+24$-hour AQI trajectories.
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

## 5. Planned Features

### Checkpoint 1: Foundation (Current)
- [x] Comprehensive repository structure and environment configuration templates.
- [x] Proposed system architecture and data-flow documentation.
- [x] Interactive React + TypeScript + Vite frontend dashboard shell.
- [x] Modular UI components based on environmental intelligence design references.
- [x] Representative demonstration telemetry data and simulated forecast curves.
- [x] FastAPI backend scaffold with health endpoints, CORS middleware, and Pydantic schemas.
- [x] Machine learning pipeline directory structure with stubbed data loaders, feature extractors, and trainers.
- [x] Smoke tests for backend and ML pipeline modules.

### Checkpoint 2: Data Pipeline & Baseline ML (Planned)
- [ ] Ingestion of historical CPCB / OpenAQ tabular datasets into `ml/data/raw/`.
- [ ] Exploratory data analysis (EDA) notebooks tracking seasonal and diurnal trends.
- [ ] Automated missing value imputation and sliding-window lag feature generation.
- [ ] Training baseline persistence and linear regression models.
- [ ] Initial scikit-learn Random Forest / Gradient Boosting regressor benchmarks.

### Checkpoint 3: Full Integration & Route Optimization (Planned)
- [ ] End-to-end connection between FastAPI prediction endpoints and trained model weights.
- [ ] Live external API telemetry polling with caching.
- [ ] Algorithmic exposure calculation for road graph routes.
- [ ] Automated model evaluation reporting (MAE, RMSE, $R^2$).

---

## 6. Proposed Technology Stack

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

The diagram below outlines the end-to-end data lifecycle from sensor ingestion through machine-learning inference to the user-facing interface:

```mermaid
flowchart LR
    A["Raw Data Sources\n(CPCB, OpenAQ, Weather)"] --> B["Data Validation & Imputation\n(ml/src/data/loader.py)"]
    B --> C["Feature Engineering\n(Lags, Diurnal, Meteorological)"]
    C --> D["Model Training & Evaluation\n(Random Forest / Gradient Boost)"]
    D --> E["Saved Model Artifact\n(ml/models/*.pkl)"]
    E --> F["FastAPI Prediction API\n(backend/app/main.py)"]
    F --> G["React Dashboard\n(frontend/src/)"]
    G --> H["Actionable Insights\n(Forecasts, Alerts, Route Planner)"]
```

*For an in-depth breakdown of layer responsibilities and expected inputs/outputs, refer to the [System Architecture Document](docs/architecture.md).*

---

## 8. Project Folder Structure

The repository is structured to enable independent, modular development across our four-member team:

```
EcoPredict/
├── README.md                      # Comprehensive project overview and setup guide
├── .gitignore                     # Multi-environment ignore file (Python, Node, ML artifacts)
├── .env.example                   # Environment variable template with safe placeholders
├── docs/
│   ├── architecture.md            # Detailed system architecture and interface specification
│   └── ui-design.md               # UI design system, color tokens, and layout guidelines
├── frontend/                      # React + TypeScript + Vite web client
│   ├── public/                    # Static web assets
│   ├── src/
│   │   ├── assets/                # Local images and graphic assets
│   │   ├── components/            # Reusable UI primitives (Header, Badges, Modals)
│   │   │   └── common/
│   │   ├── features/              # Modular domain features
│   │   │   └── dashboard/         # Dashboard cards, Leaflet map, forecast & trend charts
│   │   ├── layouts/               # Page wrapper layouts
│   │   ├── pages/                 # Top-level routed pages
│   │   ├── services/              # API clients and mock telemetry fixtures
│   │   ├── types/                 # Shared TypeScript interfaces (AQI, Stations, Forecasts)
│   │   ├── utils/                 # Severity calculators and formatting utilities
│   │   ├── App.tsx                # Root application container
│   │   ├── main.tsx               # DOM mounting entrypoint
│   │   └── index.css              # Tailwind base styles and dark theme overrides
│   ├── package.json               # Frontend dependencies and run scripts
│   ├── vite.config.ts             # Vite build and dev-server configuration
│   └── tailwind.config.js         # Tailwind theme extension and custom color tokens
├── backend/                       # FastAPI REST microservice
│   ├── app/
│   │   ├── api/                   # API routing layer
│   │   │   └── routes/            # Route modules (health, aqi endpoints)
│   │   ├── core/                  # Application configuration and settings
│   │   ├── schemas/               # Pydantic data contracts and models
│   │   ├── services/              # Business logic and mock service layers
│   │   └── main.py                # FastAPI application initialization and CORS setup
│   └── requirements.txt           # Python backend dependencies
├── ml/                            # Machine Learning & Data Science pipeline
│   ├── data/
│   │   ├── raw/                   # Raw sensor datasets (git-ignored via .gitkeep)
│   │   └── processed/             # Cleaned feature-engineered datasets
│   ├── notebooks/                 # Exploratory data analysis (EDA) notebooks
│   ├── src/                       # Production ML pipeline code
│   │   ├── data/                  # Ingestion and validation scripts
│   │   ├── features/              # Time-lag and weather feature transformers
│   │   ├── training/              # Model training and cross-validation runners
│   │   └── evaluation/            # Performance benchmarking and metric calculations
│   ├── models/                    # Serialized model weights (git-ignored via .gitkeep)
│   ├── reports/                   # Model performance evaluation artifacts
│   └── requirements.txt           # Python data science dependencies
└── tests/                         # Unit and smoke test suites
    ├── backend/                   # FastAPI endpoint and service tests
    └── ml/                        # ML pipeline and feature extraction tests
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
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite local development server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to `http://localhost:5173`.
5. To run a production type-check and build:
   ```bash
   npm run build
   ```

---

### Step C: Backend Setup
1. From the project root, navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the FastAPI development server:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
5. View interactive API documentation in your browser at `http://127.0.0.1:8000/docs`.

---

### Step D: Machine Learning Environment
1. Navigate to the `ml/` directory:
   ```bash
   cd ml
   ```
2. Install data science requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch JupyterLab for exploratory data analysis (EDA):
   ```bash
   jupyter lab
   ```

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
| `OPENAQ_API_KEY` | *(Placeholder)* | API key for external OpenAQ data ingestion (Checkpoint 2) |
| `OPENWEATHER_API_KEY` | *(Placeholder)* | API key for ambient weather telemetry (Checkpoint 2) |
| `MODEL_ARTIFACTS_DIR` | `ml/models` | Local directory for storing serialized model weights |

> [!CAUTION]
> Never commit active credentials, production API keys, or private tokens to Git. The `.gitignore` file is configured to safeguard `.env` files automatically.

---

## 11. API Documentation (Placeholder Contract)

Interactive OpenAPI (Swagger) documentation is accessible at `http://127.0.0.1:8000/docs` when the backend is running.

| Method | Endpoint | Description | Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Returns service health status and checkpoint version. | **Implemented** |
| `GET` | `/api/aqi/summary` | Returns current AQI reading, category, and pollutant metrics. | **Implemented (Mock)** |
| `GET` | `/api/aqi/stations` | Returns list of geographic monitoring stations with readings. | **Implemented (Mock)** |
| `GET` | `/api/aqi/forecast` | Returns $+24$-hour forward predictions with confidence intervals. | *Planned (Checkpoint 2)* |
| `POST` | `/api/routes/exposure` | Computes cumulative particulate exposure across transit alternatives. | *Planned (Checkpoint 3)* |

---

## 12. Data Sources & Attribution (Placeholder)

EcoPredict plans to ingest ambient air quality and meteorological telemetry from the following public and open-access sources in subsequent checkpoints:

1. **Central Pollution Control Board (CPCB) / National Air Quality Index (NAQI)**:
   - Official ambient air quality monitoring network across Indian metropolitan areas.
   - Pollutants tracked: $PM_{2.5}, PM_{10}, NO_2, SO_2, CO, O_3$.
2. **OpenAQ Platform**:
   - Aggregated global open physical air quality data platform ([openaq.org](https://openaq.org)).
3. **OpenWeather / ERA5 Reanalysis**:
   - Meteorological data feeds providing temperature, humidity, wind speed, wind direction, and surface pressure.

---

## 13. Machine-Learning Workflow

```
[ Raw CSV / API Feeds ]
           │
           ▼
[ ml/src/data/loader.py ] ──> Ingests datasets, validates timestamps, handles outliers
           │
           ▼
[ ml/src/features/engineer.py ] ──> Computes lag features (t-1 to t-24), rolling averages, cyclical encodings
           │
           ▼
[ ml/src/training/train.py ] ──> Fits Random Forest / Gradient Boosting regressors with time-series CV
           │
           ▼
[ ml/src/evaluation/evaluate.py ] ──> Evaluates MAE, RMSE, sMAPE against persistence baseline
           │
           ▼
[ ml/models/aqi_model.pkl ] ──> Serialized model artifacts loaded into FastAPI prediction service
```

*Status Note: Pipeline modules are scaffolded with clean object-oriented interfaces. Actual training on real historical data is scheduled for Checkpoint 2.*

---

## 14. Testing Instructions

### Run Python Smoke Tests
Smoke tests are located in `tests/` and verify configuration, schema integrity, and ML module interfaces without requiring external dependencies:

```bash
python -c "
import tests.backend.test_health as tb
tb.test_settings_initialization()
tb.test_aqi_service_severity_categories()
tb.test_aqi_demo_summary()
print('✓ Backend tests passed!')

import tests.ml.test_data_loader as tm
tm.test_data_loader_initialization()
tm.test_feature_engineer_transform()
tm.test_model_trainer_pipeline()
tm.test_model_evaluator()
print('✓ ML tests passed!')
"
```

When `pytest` is installed in your virtual environment:
```bash
pytest tests/
```

### Run Frontend Type Check & Build Test
```bash
cd frontend
npm run build
```

---

## 15. Team Contributions

Our hackathon team consists of four undergraduate students. Responsibilities are divided to ensure clear ownership and parallel progress:

| Team Member | Role Focus | Primary Responsibilities |
| :--- | :--- | :--- |
| **Member 1 (Prince)** | **Fullstack Lead & Coordination** | Repository management, project architecture, FastAPI service orchestration, and integration. |
| **Member 2** | **Frontend & UI/UX Developer** | React components, Tailwind styling, Recharts visualization, and responsive design. |
| **Member 3** | **Data Engineer & Pipeline Lead** | Ingestion from CPCB/OpenAQ, automated data cleaning, missing value imputation, and feature engineering. |
| **Member 4** | **Machine Learning Specialist** | Time-series forecasting models, baseline benchmarking, evaluation metrics, and model serialization. |

---

## 16. Current Project Status & Roadmap

```
[ Checkpoint 1: Foundation ] ──▶ [ Checkpoint 2: Data & ML ] ──▶ [ Checkpoint 3: Integration ]
       (COMPLETED)                     (UPCOMING)                       (UPCOMING)
```

### Status Matrix:
- **Implemented in Checkpoint 1**:
  - Full project folder hierarchy and multi-layer configuration.
  - Interactive React + TypeScript frontend dashboard with dark slate visual theme.
  - Leaflet geospatial map with simulated monitoring stations and hotspot dispersion rings.
  - 24-hour predictive forecast curve and historical telemetry trend chart with metric toggle.
  - Specific pollutant breakdown ($PM_{2.5}, PM_{10}, NO_2, SO_2, CO, O_3$) with NAAQS standard limit comparisons.
  - Route planner UI with comparative clean-corridor exposure estimates.
  - FastAPI backend scaffold with health check and mock AQI summary endpoints.
  - ML pipeline skeletons (`loader`, `engineer`, `train`, `evaluate`).
  - System architecture and UI design documentation.
- **Planned for Checkpoint 2**:
  - Acquisition of historical CPCB air quality datasets.
  - Feature extraction pipeline implementation.
  - Supervised machine learning model training and evaluation benchmarks.
- **Planned for Checkpoint 3**:
  - Live prediction endpoint serving serialized model outputs.
  - End-to-end frontend and backend API integration.

---

## 17. Limitations & Future Improvements

### Current Limitations:
1. **Scaffold Telemetry**: Visualizations currently render illustrative demonstration data labeled as `Demo Data` or `Simulated Preview`.
2. **Offline Routing**: The clean route planner uses a simulated heuristic rather than a live OpenStreetMap / OSRM graph routing engine.
3. **Station Coverage**: Demonstration coordinates focus on Delhi NCR; nationwide station coverage requires live API ingestion.

### Planned Future Improvements:
- **Hyperlocal Satellite Ingestion**: Incorporate Sentinel-5P tropospheric column NO2 measurements.
- **Deep Learning Sequence Models**: Explore Temporal Convolutional Networks (TCN) or LSTM architectures for multi-day horizons.
- **Push Alerts & PWA**: Progressive Web App capabilities for localized push notifications during sudden particulate anomalies.

---

## 18. License

This project is developed as part of a hackathon submission. Proposed under the **MIT License** — see [LICENSE](LICENSE) (placeholder) for details.
