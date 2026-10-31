# EcoPredict — UI/UX Design System & Specification

This document details the visual design direction, color tokens, layout hierarchy, and component specifications for the **EcoPredict** frontend dashboard.

---

## 1. Visual Direction & Design Philosophy

The EcoPredict user interface is designed as an **environmental intelligence platform** rather than a generic sustainability landing page. It emphasizes:
- **High Data Density without Clutter**: Clear grouping of metrics, concise spacing, and structured cards.
- **Dark Charcoal / Deep Slate Surfaces**: Reduces eye fatigue during nighttime telemetry monitoring, providing contrast for map overlays and charts.
- **Restrained Accents**: Cool emeralds (`#10b981`) and cyans (`#06b6d4`) for positive actions and predictive indicators, avoiding saturated neon clutter.
- **Accessible AQI Severity System**: Colors are always paired with explicit text labels, icons, and numerical ranges—never relying on color alone.
- **Responsive Layout**: Designed for laptop displays, tablet devices, and mobile screens.

---

## 2. Color Palette & Semantic Tokens

### Surface & Base Colors
| Token | Hex Value | Tailwind Class | Usage |
| :--- | :--- | :--- | :--- |
| **Canvas Background** | `#020617` | `bg-slate-950` | Full-page base background |
| **Surface Card** | `#0f172a` | `bg-slate-900` | Metric cards, panels, containers |
| **Surface Subdued** | `#020617` (80%) | `bg-slate-950/80` | Inner inputs, table rows, legends |
| **Border Normal** | `#1e293b` | `border-slate-800` | Card borders, dividers |
| **Border Focus** | `#334155` | `border-slate-700` | Hover states, active inputs |
| **Text Primary** | `#f8fafc` | `text-slate-100` | Headings, key figures |
| **Text Muted** | `#94a3b8` | `text-slate-400` | Subtitles, units, meta timestamps |

### Air Quality Index (AQI) Severity Scale
Following the Central Pollution Control Board (CPCB) and standard environmental health scales:

| Severity Category | Range | Color Hex | Tailwind Accent | Health Implication |
| :--- | :--- | :--- | :--- | :--- |
| **Good** | $0 - 50$ | `#22c55e` | `text-emerald-400` / `bg-emerald-500/10` | Minimal impact |
| **Moderate** | $51 - 100$ | `#eab308` | `text-yellow-400` / `bg-yellow-500/10` | Minor breathing discomfort to sensitive people |
| **Poor** | $101 - 200$ | `#f97316` | `text-orange-400` / `bg-orange-500/10` | Breathing discomfort to most people on prolonged exposure |
| **Very Poor** | $201 - 300$ | `#ef4444` | `text-red-400` / `bg-red-500/10` | Respiratory illness on prolonged exposure |
| **Severe** | $301 - 400$ | `#a855f7` | `text-purple-400` / `bg-purple-500/10` | Affects healthy people and seriously impacts those with existing diseases |
| **Hazardous** | $401+$ | `#881337` | `text-rose-300` / `bg-rose-950/40` | Emergency condition; entire population likely affected |

---

## 3. Component Hierarchy & Layout

```
┌────────────────────────────────────────────────────────────────────────┐
│ Top Navigation: Logo | Location Selector | Live Anomaly Pill | Demo Tag│
├────────────────────────────────────────────────────────────────────────┤
│ KPI Summary Cards (4-column grid):                                    │
│ [ Current Avg AQI ]  [ 12h Prediction ]  [ Main Pollutant ]  [ Advice] │
├───────────────────────────────────────┬────────────────────────────────┤
│                                       │ Route Cleaner:                 │
│ Interactive Leaflet Map:              │ [ Start Point ]                │
│ - Geo-referenced stations             │ [ Destination ]                │
│ - Hotspot dispersion rings            │ [ Calculate Cleanest Route ]   │
│ - Severity Legend                     ├────────────────────────────────┤
│ - Selected station inspect drawer     │ Hotspot Analysis:              │
│                                       │ - Traffic / Stubble / Industry │
│                                       │ - Localized Area Alert         │
├───────────────────────────────────────┴────────────────────────────────┤
│ Predictive & Historical Analysis:                                      │
│ [ 24h AQI Forecast Chart (Bounds) ]   [ Historical 24h Trend Chart ]   │
├───────────────────────────────────────┬────────────────────────────────┤
│ Specific Pollutant Concentrations:    │ Sectoral Source Apportionment: │
│ [ PM2.5 | PM10 | NO2 | SO2 | CO | O3 ]│ [ Donut Chart Breakdown ]      │
└───────────────────────────────────────┴────────────────────────────────┘
```

---

## 4. Key Design References & Inspirations

Based on the provided design reference (*Delhi Air Health Companion*):
1. **Anomaly Banner**: Prominently placed at the top-right of the header with a warning icon, summarizing sudden localized particulate spikes (e.g. Okhla industrial corridor).
2. **Dual-Horizon Insights**: Presenting both the current snapshot (observed average AQI) and the immediate predictive horizon (12h/24h prediction with confidence rating).
3. **Clean Route Exposure Planner**: Provides proactive utility by computing transit alternatives that reduce cumulative inhalation of toxic particulate matter.
4. **Source Apportionment**: Breaks down contributing factors (Vehicular traffic, stubble/biomass burning, industrial dust) so citizens and policymakers understand the drivers of pollution.

---

## 5. Accessibility & Data Transparency Principles

1. **Clear Demo Labeling**: Every chart, card, and map layer in Checkpoint 1 carries a visible `Demo Data` or `Simulated Preview` badge to ensure academic integrity during hackathon evaluation.
2. **Text + Symbol Redundancy**: An AQI value of `234` is accompanied by both an orange indicator badge and the explicit word `Poor` to ensure readability for colorblind users.
3. **Responsive Flow**: Uses CSS Grid and Flexbox with Tailwind break points (`sm`, `md`, `lg`) allowing full usability across desktop workstations and mobile devices.
