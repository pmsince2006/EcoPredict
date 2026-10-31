# EcoPredict — Backend API Contract & Interface Specification

This document defines the HTTP REST API contracts, request/response JSON schemas, data status taxonomy, and integration protocols between the **EcoPredict FastAPI Backend** and the **React Dashboard**.

---

## 1. Architectural Principles & Data Status Taxonomy

To ensure scientific honesty and prevent accidental misrepresentation of model accuracy or sensor telemetry, EcoPredict enforces an explicit **Data Status Taxonomy** across all API responses:

| `data_status` Value | Semantic Meaning | Criteria Required for Activation |
| :--- | :--- | :--- |
| **`real_observation`** | Verified ground-truth sensor measurement. | Must be ingested from a verified station network (e.g. CPCB CCR or OpenAQ). |
| **`real_data_forecast`** | Forward prediction produced by a model trained on verified real observations. | Requires verified dataset, chronological evaluation benchmarks, and artifact verification. |
| **`demo_preview`** | Illustrative mock or prediction from a model trained on synthetic test fixtures. | Used for Checkpoint 1–3 UI development and software integration testing. |
| **`unavailable`** | Required model weights, dataset, or telemetry feed are not accessible. | Returned when requested artifacts or sources cannot be located. |

---

## 2. Global API Configuration

- **Base URL**: `http://localhost:8000/api`
- **Frontend Environment Variable**: `VITE_API_BASE_URL` (configured in `.env.example`)
- **Protocol**: HTTP/1.1 (JSON payloads, UTF-8 encoded)
- **Timezone**: All timestamps are formatted as ISO 8601 strings (`YYYY-MM-DDTHH:MM:SSZ` or with timezone offset).

---

## 3. Endpoint Specifications

### 3.1 Health Check & Provenance Introspection
* **Endpoint**: `GET /api/health`
* **Purpose**: Inspect service uptime, API version, model loading status, and artifact provenance.

#### Response (`200 OK`)
```json
{
  "status": "healthy",
  "service": "EcoPredict Backend API",
  "version": "0.3.0-checkpoint3",
  "checkpoint": "Checkpoint 3 — Safe Backend Inference & Integration",
  "data_status": "demo_preview",
  "model_loaded": true,
  "model_provenance": "synthetic_fixture",
  "real_data_validated": false,
  "environment": "development"
}
```

---

### 3.2 Current AQI Summary
* **Endpoint**: `GET /api/aqi/summary`
* **Query Parameters**:
  - `location` *(string, optional, default: `"Delhi NCR"`)*: Name of the monitoring area.

#### Response (`200 OK`)
```json
{
  "location_name": "Delhi NCR",
  "aqi": 234,
  "category": "Poor",
  "severity_color": "#f97316",
  "primary_pollutant": "PM 2.5",
  "primary_concentration": "92 µg/m³",
  "twelve_hour_prediction": 164,
  "twelve_hour_category": "Poor",
  "prediction_confidence": "88%",
  "health_advice": "Wear N95 mask outdoors today. Sensitive groups should avoid prolonged exertion.",
  "change_rate": "+5% from 1hr ago",
  "data_status": "demo_preview",
  "is_demo_data": true,
  "pollutants": {
    "pm25": 92.4,
    "pm10": 168.0,
    "no2": 44.2,
    "so2": 18.1,
    "co": 1.4,
    "o3": 32.5
  },
  "last_updated": "2026-11-01T00:55:00Z"
}
```

---

### 3.3 Monitoring Stations Telemetry
* **Endpoint**: `GET /api/aqi/stations`
* **Purpose**: Returns geo-referenced sensor station coordinates, current AQI, and status.

#### Response (`200 OK`)
```json
{
  "stations": [
    {
      "id": "st-1",
      "name": "Connaught Place",
      "lat": 28.6315,
      "lng": 77.2167,
      "aqi": 210,
      "category": "Poor",
      "status": "Active",
      "main_pollutant": "PM 2.5 (88 µg/m³)"
    },
    {
      "id": "st-2",
      "name": "Okhla Industrial Area",
      "lat": 28.5355,
      "lng": 77.2732,
      "aqi": 312,
      "category": "Severe",
      "status": "Alert",
      "main_pollutant": "PM 2.5 (182 µg/m³)"
    }
  ],
  "data_status": "demo_preview",
  "is_demo_data": true,
  "count": 2
}
```

---

### 3.4 Multi-Horizon AQI Model Forecast
* **Endpoint**: `GET /api/aqi/forecast`
* **Query Parameters**:
  - `location` *(string, optional, default: `"Delhi NCR"`)*: Target region.
  - `horizon` *(integer, optional, default: `24`, min: `1`, max: `72`)*: Forecast horizon in hours.
  - `allow_demo` *(boolean, optional, default: `true`)*: If set to `false` when only demo models exist, returns `data_status: "unavailable"`.

#### Response (`200 OK` — Demo Model Mode)
```json
{
  "target_variable": "pm25",
  "target_unit": "µg/m³",
  "forecast_horizon_hours": 24,
  "generated_at": "2026-11-01T00:58:00Z",
  "location_name": "Delhi NCR",
  "station_id": "DL001_ANAND_VIHAR",
  "data_status": "demo_preview",
  "is_demo_model": true,
  "real_data_validated": false,
  "model_version": "baseline_random_forest.pkl",
  "model_provenance": "synthetic_fixture",
  "model_mae": 7.943,
  "model_rmse": 8.494,
  "forecast_points": [
    {
      "time": "01:00",
      "predicted_pm25": 142.3,
      "predicted_aqi": 317,
      "lower_bound_pm25": 130.1,
      "upper_bound_pm25": 154.5,
      "category": "Severe"
    }
  ],
  "disclaimer": "DEMO MODEL PREVIEW: Forecast generated using baseline Random Forest trained on synthetic test fixture. Values are illustrative and must NOT be cited as real-world atmospheric predictions."
}
```

#### Response (`200 OK` — When Real Data is Required but Unavailable)
```json
{
  "target_variable": "pm25",
  "target_unit": "µg/m³",
  "forecast_horizon_hours": 24,
  "location_name": "Delhi NCR",
  "data_status": "unavailable",
  "is_demo_model": true,
  "real_data_validated": false,
  "forecast_points": [],
  "disclaimer": "Real-data forecasting is unavailable. The current model is an unvalidated demonstration artifact."
}
```

---

## 4. Error Handling & Status Codes

| Status Code | Reason | Example Response Body |
| :--- | :--- | :--- |
| `400 Bad Request` | Invalid query parameter (e.g. `horizon=100`) | `{"detail": "Horizon hours must be between 1 and 72."}` |
| `422 Unprocessable Entity` | Pydantic type mismatch (e.g. `horizon=abc`) | `{"detail": [{"loc": ["query", "horizon"], "msg": "Input should be a valid integer"}]}` |
| `500 Internal Error` | Uncaught server exception | `{"detail": "Inference failure: <sanitized error message>"}` |

> [!NOTE]
> Internal filesystem paths, stack traces, and local directory configurations are never returned in public error payloads.

---

## 5. Security & Model Deserialization Policy

1. **Pickle Execution Warning**: Python's `pickle` library is vulnerable to arbitrary code execution when loading untrusted data.
2. **Fixed Anchor**: Model weights are loaded strictly from `settings.MODEL_ARTIFACTS_DIR`. Client requests cannot pass filenames or paths to the server.
3. **Artifact Integrity**: The server verifies that `model_metadata.json` exists, is valid JSON, and that its feature count matches `model.n_features_in_` before invoking predictions.

---

## 6. Checklist for Activating Real-Data Model Forecasts

To graduate from `data_status="demo_preview"` to `data_status="real_data_forecast"`, complete the following 8 steps:

- [ ] **Step 1: Ingest Verified Dataset**: Download historical hourly CPCB CAAQMS or OpenAQ v3 observations for target stations.
- [ ] **Step 2: Record Provenance**: Document exact station ID, geographic coordinates, units, sampling interval, and download timestamp in `docs/dataset.md`.
- [ ] **Step 3: Run Data Quality Checks**: Verify zero negative sensor calibration errors, parse UTC/IST timestamps, and remove duplicate timestamps.
- [ ] **Step 4: Chronological Split**: Partition chronologically (70% train, 15% validation, 15% held-out test). Shuffling is prohibited.
- [ ] **Step 5: Train & Benchmark**: Train Random Forest on lagged features and compare against persistence baseline ($y_{t+h} = y_t$).
- [ ] **Step 6: Record Metrics**: Record test MAE, RMSE, $R^2$, and sample count in `model_metadata.json`.
- [ ] **Step 7: Update Metadata**: Set `training_data_provenance: "verified_real_data"`, `is_demo_model: false`, and `real_data_validated: true`.
- [ ] **Step 8: Enable Real-Data Serving**: Restart backend service; `ModelService` will automatically detect validated provenance and serve predictions with `data_status: "real_data_forecast"`.
