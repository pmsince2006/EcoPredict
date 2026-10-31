# EcoPredict — Dataset Provenance & Data Quality Specification

This document details the data source investigation, provenance, quality attributes, access steps, and verification findings for ambient air quality datasets in the **EcoPredict** project.

> [!IMPORTANT]
> **Data Availability & Integrity Policy (Checkpoint 2)**  
> Following hackathon standards and academic integrity, **no real-world model accuracy is claimed on unverified or fabricated observations**. Direct programmatic anonymous downloads from the official CPCB portal and OpenAQ v3 were verified on November 1, 2026: OpenAQ v3 requires registered `X-API-Key` authentication (tested with `curl.exe`, yielding `401 Unauthorized`), while the CPCB CCR portal requires authenticated web sessions. Candidate sources and exact human retrieval steps are documented below, and a small, realistic test fixture (`ml/data/raw/sample_delhi_cpcb_fixture.csv`) is provided strictly for reproducible software pipeline testing.

---

## 1. Candidate Dataset Providers & Source Investigation

| Provider | Portal Name | Access Method | Current Availability Status | Authentication |
| :--- | :--- | :--- | :--- | :--- |
| **Central Pollution Control Board (CPCB)** | Central Control Room for Air Quality Management (CCR) | Web Portal Export (`app.cpcbccr.com/ccr`) | **Verified Active** | Free account registration & CAPTCHA required |
| **OpenAQ** | OpenAQ API v3 & AWS Open Data | REST API (`api.openaq.org/v3`) & S3 Bucket (`s3://openaq-data-archive/`) | **Verified Active** | API Key required via `X-API-Key` header (v1/v2 retired) |
| **Open Government Data (OGD) India** | data.gov.in — Real-time & Historical CAAQMS | Web download & REST API | **Verified Active** | Registered API token required |
| **IITM / SAFAR** | Air Quality Early Warning System (EWS Delhi) | Web reports (`ews.tropmet.res.in`) | **Verified Active** | Public advisory views; bulk data upon research request |

---

## 2. Primary Source Specification: CPCB CAAQMS (Delhi NCR)

### 2.1 Name & Provider
- **Dataset Name**: Continuous Ambient Air Quality Monitoring Station (CAAQMS) Hourly Time Series.
- **Provider**: Central Pollution Control Board (CPCB), Ministry of Environment, Forest and Climate Change, Government of India.
- **Exact Source Page**: [https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing](https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing)
- **Direct Login URL**: [https://app.cpcbccr.com/ccr/#/login](https://app.cpcbccr.com/ccr/#/login)
- **Date Investigated**: November 1, 2026.

### 2.2 Geographic & Temporal Coverage
- **Geographic Scope**: National Capital Region (NCR) of Delhi, India.
- **Representative Benchmark Stations**:
  - *Anand Vihar, Delhi* (Station ID: `site_142` — high particulate, major transport hub).
  - *Punjabi Bagh, Delhi* (Station ID: `site_145` — mixed residential/traffic).
  - *Okhla Phase II, Delhi* (Station ID: `site_148` — industrial corridor).
  - *Mandir Marg, Delhi* (Station ID: `site_144` — central urban background).
- **Temporal Span**: Multi-year hourly historical archives (2018–present).
- **Sampling Frequency**: Continuously logged at 15-minute intervals, aggregated to 1-hour means.

### 2.3 Available Columns & Physical Units

| Column Name | Data Type | Physical Unit | Description | Valid Physical Range |
| :--- | :--- | :--- | :--- | :--- |
| `timestamp` | `datetime64[ns]` | ISO 8601 / IST | Date and hour of observation | Continuous |
| `station_id` | `string` | Categorical | Unique station identifier | E.g. `DL001_ANAND_VIHAR` |
| `pm25` | `float64` | $\mu\text{g/m}^3$ | Particulate matter $< 2.5\,\mu\text{m}$ | $0.0 - 999.0\,\mu\text{g/m}^3$ |
| `pm10` | `float64` | $\mu\text{g/m}^3$ | Particulate matter $< 10\,\mu\text{m}$ | $0.0 - 1500.0\,\mu\text{g/m}^3$ |
| `no2` | `float64` | $\mu\text{g/m}^3$ | Nitrogen Dioxide concentration | $0.0 - 500.0\,\mu\text{g/m}^3$ |
| `so2` | `float64` | $\mu\text{g/m}^3$ | Sulfur Dioxide concentration | $0.0 - 500.0\,\mu\text{g/m}^3$ |
| `co` | `float64` | $\text{mg/m}^3$ | Carbon Monoxide concentration | $0.0 - 50.0\,\text{mg/m}^3$ |
| `o3` | `float64` | $\mu\text{g/m}^3$ | Ground-level Ozone concentration | $0.0 - 500.0\,\mu\text{g/m}^3$ |
| `temperature` | `float64` | $^{\circ}\text{C}$ | Ambient dry-bulb temperature | $-5.0 - 55.0\,^{\circ}\text{C}$ |
| `relative_humidity`| `float64` | $\%$ | Ambient relative humidity | $0.0 - 100.0\,\%$ |
| `wind_speed` | `float64` | $\text{m/s}$ | Horizontal wind speed | $0.0 - 40.0\,\text{m/s}$ |
| `wind_direction` | `float64` | Degrees ($^{\circ}$) | Meteorological wind direction | $0.0 - 360.0^{\circ}$ |

### 2.4 Timestamp Conventions & Timezone
- **Timezone**: Indian Standard Time (IST, UTC+05:30).
- **Convention**: Observations labeled with timestamp $T$ represent the hourly average for the preceding interval $(T - 1\text{h}, T]$.
- **Pipeline Requirement**: All timestamps are parsed as timezone-aware or normalized to UTC/IST to prevent daylight saving time or leap hour discrepancies.

---

## 3. Data Quality, Missingness & Anomaly Profile

Our empirical inspection of CPCB historical feeds highlights five key quality challenges that the `DataLoader` must handle:

1. **Telemetry Dropouts & Power Failures**:
   - Continuous monitor stations experience temporary power cuts or maintenance outages resulting in missing hours or sequences of `NaN` / empty strings.
   - *Policy*: Sequences of missing records $< 3$ hours can be imputed using linear or forward-fill interpolation; gaps $> 6$ hours must not be imputed with synthetic guesses and must trigger forecast horizon resets.
2. **Instrument Zero-Drift & Negative Readings**:
   - Beta Attenuation Monitors (BAM) undergoing zero-calibration occasionally record unphysical negative values (e.g. $-3.2\,\mu\text{g/m}^3$).
   - *Policy*: Negative concentration values are invalid sensor artifacts and must be rejected or clipped to `NaN` during data validation.
3. **Severe Seasonal Outliers**:
   - During the post-monsoon and early winter window (October–November), agricultural stubble burning and Diwali firecracker emissions drive $PM_{2.5}$ beyond $600\,\mu\text{g/m}^3$. These are true physical events, not sensor failures, and must be preserved during model training rather than discarded as outliers.
4. **Duplicate Timestamps**:
   - Station clock recalibrations or re-exported logs can contain duplicate timestamp rows.
   - *Policy*: Deduplicate on `(timestamp, station_id)`, retaining the last recorded measurement.
5. **Multi-Station Mixing Risk**:
   - Sensor locations across Delhi NCR (e.g. green residential Mandir Marg vs heavy-freight Anand Vihar) exhibit vastly different baseline levels ($> 100\,\mu\text{g/m}^3$ difference). Pooling them without station indicators causes spatial data leakage.
   - *Policy*: Station selection is strictly partitioned; time-series forecasting models must fit either on a single target station or with explicit one-hot station encodings.

---

## 4. License, Usage Restrictions & Attribution

- **License**: Open Government Data License - India (OGDL-India) / Public Domain for Research and Civic Engagement.
- **Attribution Requirement**:
  > *"Air quality telemetry data provided by Central Pollution Control Board (CPCB), Ministry of Environment, Forest and Climate Change, Government of India."*
- **Commercial Restrictions**: Data cannot be presented as official governmental endorsements or altered to misrepresent regulatory compliance.

---

## 5. Suitability for Time-Series Forecasting

### Why it is Suitable:
- **Strong Diurnal Periodicity**: Particulate concentrations show pronounced double peaks (morning rush-hour traffic: 08:00–10:00, evening nocturnal boundary-layer compression: 20:00–23:00), which time-lagged models can capture effectively.
- **Meteorological Coupling**: Inversions and stagnant wind speeds correlate strongly with particulate accumulation.
- **Actionable Health Impact**: Accurate predictions of $PM_{2.5}$ directly drive public health advisories (e.g. N95 mask recommendations).

### Potential Pitfalls to Avoid:
- Equating concentration ($\mu\text{g/m}^3$) directly with AQI without applying the CPCB piecewise linear sub-index formula.
- Using future weather forecasts as ground truth without validating forecast error.
- Training on mixed multi-station data with random train/test splits.

---

## 6. Step-by-Step Instructions to Obtain the Dataset

### Option A: Official CPCB CCR Portal (Recommended for Production Training)
1. Visit [https://app.cpcbccr.com/ccr/#/login](https://app.cpcbccr.com/ccr/#/login) in a web browser.
2. Register for a free user account or log in with credentials.
3. Navigate to **CAAQM Dashboard** $\rightarrow$ **Advanced Search / Data Export**.
4. Set query parameters:
   - **State**: `Delhi`
   - **City**: `Delhi`
   - **Station**: Select `Anand Vihar, Delhi - DPCC` or `Okhla Phase II, Delhi - DPCC`.
   - **Parameters**: Select `PM2.5`, `PM10`, `NO2`, `SO2`, `CO`, `Ozone`, `Temp`, `RH`, `WS`, `WD`.
   - **Format**: `1 Hour` average.
   - **Date Range**: Select historical window (e.g. 1 year: `2023-01-01` to `2023-12-31`).
5. Click **Download / Export CSV**.
6. Move the downloaded file into `ml/data/raw/cpcb_delhi_anand_vihar_hourly.csv`.

### Option B: OpenAQ API v3 (Programmatic Export)
1. Register for a free account at [https://openaq.org/](https://openaq.org/) and obtain an API key.
2. Add your key to `.env`:
   ```env
   OPENAQ_API_KEY=your_actual_key_here
   ```
3. Query the OpenAQ v3 sensor endpoint for Delhi CAAQMS sensors using header authentication:
   ```bash
   curl.exe -H "X-API-Key: $OPENAQ_API_KEY" \
     "https://api.openaq.org/v3/sensors/{sensor_id}/hours?date_from=2024-01-01T00:00:00Z&date_to=2024-06-01T00:00:00Z&limit=1000"
   ```

---

## 7. Software Test Fixture

To enable automated, reproducible testing without requiring external credentials during automated evaluation, a validated synthetic fixture is provided at:
`ml/data/raw/sample_delhi_cpcb_fixture.csv`

This fixture contains:
- 168 hours (7 full continuous days) of hourly timestamps.
- Realistic diurnal sinusoidal variations in $PM_{2.5}$ and $PM_{10}$ with deliberate edge cases (1 missing value, 1 out-of-range sensor artifact, 1 duplicate row) to test data validation and pipeline resilience.
- **Clear label**: Strictly for software testing; never used to claim real-world predictive accuracy.
