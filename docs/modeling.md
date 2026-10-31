# EcoPredict — Forecasting Task Definition & Modeling Methodology

This document formalizes the mathematical problem formulation, target variable definitions, AQI standards, evaluation protocol, and data leakage safeguards for the machine learning forecasting models in **EcoPredict**.

---

## 1. Problem Formulation & Target Variable

### 1.1 Target Variable Definition
In air quality modeling, predicting raw particulate concentration ($PM_{2.5}$) is scientifically superior to predicting an aggregated index directly:
1. **Physical Quantity**: $PM_{2.5}$ (measured in $\mu\text{g/m}^3$) is a physical, continuous mass concentration governed by atmospheric dispersion, emissions, and meteorology.
2. **Sub-Index Conversion**: Once continuous $PM_{2.5}$ and $PM_{10}$ trajectories are predicted, they can be mapped to the official regulatory **National Air Quality Index (NAQI)** via standard piecewise linear sub-index formulas without information loss.

**Primary Prediction Target**:
$$y_{t+h} = \text{Concentration of } PM_{2.5} \text{ at hour } t+h \quad (\mu\text{g/m}^3)$$

### 1.2 Forecast Horizon ($h$)
- **Defensible Initial Task (Checkpoint 2)**: $h = +1\text{h}$ and $h = +6\text{h}$ short-term predictive horizons.
  - *Justification*: Forecasting 24 hours ahead using only auto-regressive particulate lags without prospective numerical weather forecasts (e.g. wind shifts, rainfall) suffers from severe error compounding. Establishing verified $+1\text{h}$ and $+6\text{h}$ baselines first provides an interpretable, defensible benchmark.
- **Extended Task (Checkpoint 3)**: Multi-horizon recursive or direct $+24\text{h}$ forecast with confidence intervals.

---

## 2. Indian National AQI (NAQI) Standard vs Concentration

> [!WARNING]
> **Critical Distinction**: Particulate concentration ($\mu\text{g/m}^3$) must **never** be equated directly to the Air Quality Index (AQI).

The Central Pollution Control Board (CPCB) calculates the overall AQI by computing individual pollutant sub-indices ($I_p$) via piecewise linear interpolation and taking the maximum sub-index:
$$\text{AQI} = \max(I_{\text{PM2.5}}, I_{\text{PM10}}, I_{\text{NO2}}, I_{\text{SO2}}, I_{\text{CO}}, I_{\text{O3}})$$

For a single pollutant with observed concentration $C_p$, the sub-index $I_p$ is calculated as:
$$I_p = I_{\text{low}} + \frac{I_{\text{high}} - I_{\text{low}}}{B_{\text{high}} - B_{\text{low}}} \times (C_p - B_{\text{low}})$$
where $[B_{\text{low}}, B_{\text{high}}]$ is the concentration breakpoint bracket, and $[I_{\text{low}}, I_{\text{high}}]$ is the corresponding AQI index bracket.

### CPCB Breakpoint Table for $PM_{2.5}$ (24-hour average)
| Category | AQI Range ($I_{\text{low}} - I_{\text{high}}$) | $PM_{2.5}$ Breakpoint ($B_{\text{low}} - B_{\text{high}}$, $\mu\text{g/m}^3$) |
| :--- | :--- | :--- |
| **Good** | $0 - 50$ | $0 - 30$ |
| **Satisfactory / Moderate** | $51 - 100$ | $31 - 60$ |
| **Moderate / Poor** | $101 - 200$ | $61 - 90$ |
| **Poor / Very Poor** | $201 - 300$ | $91 - 120$ |
| **Severe** | $301 - 400$ | $121 - 250$ |
| **Hazardous** | $401 - 500$ | $250+$ |

EcoPredict implements this calculation in utility functions so users receive both physical concentrations and official CPCB AQI classifications.

---

## 3. Geographic Scope & Station Selection Policy

- **Single-Station Continuity**: Sensor data is strictly segmented by `station_id`.
- **No Uncontrolled Spatial Pooling**: We do **not** pool measurements from multiple monitoring stations into a single time series without explicit station indicators, because station geographic elevation, traffic proximity, and localized industrial sources create severe distribution shifts.
- **Primary Benchmark Station**: Anand Vihar, Delhi (`site_142`), known for consistent logging and high particulate variance.

---

## 4. Feature Space & Data Leakage Prevention

### 4.1 Features Available at Prediction Time ($t$)
All features must be constructed exclusively from information available at or before forecast origin $t$:

1. **Auto-regressive Lag Features**:
   - $PM_{2.5}(t)$, $PM_{2.5}(t-1)$, $PM_{2.5}(t-2)$, $PM_{2.5}(t-3)$, $PM_{2.5}(t-6)$, $PM_{2.5}(t-12)$, $PM_{2.5}(t-24)$.
2. **Lagged Ratio / Acceleration**:
   - $\Delta PM_{2.5} = PM_{2.5}(t) - PM_{2.5}(t-1)$ (rate of change over the last hour).
3. **Trailing Rolling Statistics** (Strictly Backward-Looking):
   - 3-hour trailing mean: $\frac{1}{3}\sum_{k=0}^{2} PM_{2.5}(t-k)$
   - 6-hour trailing mean: $\frac{1}{6}\sum_{k=0}^{5} PM_{2.5}(t-k)$
   - 24-hour trailing mean: $\frac{1}{24}\sum_{k=0}^{23} PM_{2.5}(t-k)$
4. **Cyclical Temporal Features**:
   - $\sin(2\pi \times \text{hour} / 24)$ and $\cos(2\pi \times \text{hour} / 24)$
   - $\sin(2\pi \times \text{dayofweek} / 7)$ and $\cos(2\pi \times \text{dayofweek} / 7)$
   - Weekend flag ($1$ if Saturday/Sunday, else $0$).

### 4.2 Prohibited Transformations (Leakage Safeguards)
- **Centered Rolling Windows**: Using $\text{rolling}(window=3, center=True)$ is strictly banned because it leaks $t+1$ observations into prediction time $t$.
- **Global Imputation**: Imputing missing values using the mean or median of the entire dataset (including validation/test sets) is prohibited. Imputation parameters must be computed strictly on the training partition.
- **Random Shuffling**: Random train/test splits (e.g. `train_test_split(shuffle=True)`) are strictly banned in time-series forecasting.

---

## 5. Chronological Train, Validation, and Test Splitting

To replicate real-world deployment where the model is evaluated on future unseen periods, data is partitioned chronologically:

```
Timeline: [ ────────── Train (70%) ────────── ][ ── Val (15%) ── ][ ── Test (15%) ── ]
Time:     t_0                                 t_train             t_val             t_end
```

1. **Training Set ($70\%$)**: Earliest chronological block used to fit feature transformations and regression algorithms.
2. **Validation Set ($15\%$)**: Intermediate block used for hyperparameter tuning and model selection.
3. **Test Set ($15\%$)**: Latest chronological block held out completely until final benchmark reporting.

---

## 6. Baselines & Evaluation Metrics

### 6.1 Baselines
1. **Persistence Baseline**:
   $$\hat{y}_{t+h} = y_t$$
   The prediction for $h$ hours ahead is simply the latest observed value at time $t$. This is a rigorous benchmark for environmental time-series, particularly at short horizons ($h \le 3\text{h}$).
2. **Historical Mean Baseline**:
   $$\hat{y}_{t+h} = \bar{y}_{\text{train}}$$
   The mean target value observed during the training period.

### 6.2 Primary Regressor Model
- **Random Forest Regressor / Ridge Linear Model**:
  Non-linear ensemble combining decision trees on lagged features and cyclical temporal indicators.

### 6.3 Evaluation Metrics
- **Mean Absolute Error (MAE)**:
  $$\text{MAE} = \frac{1}{N}\sum_{i=1}^N |y_i - \hat{y}_i| \quad (\mu\text{g/m}^3)$$
  Directly interpretable average magnitude of prediction error in concentration units.
- **Root Mean Squared Error (RMSE)**:
  $$\text{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2} \quad (\mu\text{g/m}^3)$$
  Penalizes large errors, essential for evaluating model reliability during severe hazardous spike events.
- **Mean Absolute Percentage Error (MAPE)**:
  Percentage relative error where valid ($y_i > 0$).
