# 🌌 Asteroid Risk Radar

A data pipeline that fetches near-Earth asteroid data from NASA's NeoWs API, cleans it, computes a custom risk score for each asteroid, and produces visualisations and an automated summary report.

---

## 1. Project Overview

Asteroid Risk Radar collects real close-approach data for 2025 from NASA, engineers a composite risk score from physical and orbital features, and surfaces the riskiest objects through automated charts and an exploratory notebook.

---

## 2. Problem Statement

NASA tracks thousands of near-Earth objects every year. Raw orbital data is hard to interpret directly — an asteroid can be large but far away, or small but dangerously close. This project answers: which asteroids pose the greatest combined threat, and do risk levels cluster in certain months or velocity ranges?

---

## 3. Data Source

- API: NASA NeoWs — Near Earth Object Web Service (https://api.nasa.gov/)
- Endpoint: GET /neo/rest/v1/feed
- Date range: 2025-01-01 to 2025-12-31
- Total records: 1 442 unique asteroids (after deduplication)
- Format: JSON → Pandas DataFrame → CSV

---

## 4. Technologies Used

- requests        : NASA API calls
- pandas          : Data cleaning and feature engineering
- numpy           : Normalisation arithmetic
- matplotlib      : Visualisations
- seaborn         : Visualisations
- python-dotenv   : Secure API key loading from .env
- jupyter         : Exploratory analysis notebook


---

## 5. Data Collection Process

The NeoWs API accepts a maximum window of 7 days per request. fetch_data.py splits the full year into 7-day batches, sends one request per batch with a 1-second delay for rate limit protection, and merges all responses into a single JSON file saved at data/raw/nasa_neo_raw.json.

---

## 6. Data Cleaning

Performed in src/clean_data.py:

- Flattened nested JSON into a tabular structure
- Extracted all 9 required fields per asteroid:
  id, name, estimated_diameter_min, estimated_diameter_max,
  is_potentially_hazardous_asteroid, close_approach_date,
  relative_velocity_km_s, miss_distance_km, orbiting_body
- Computed average_diameter = (min + max) / 2
- Parsed close_approach_date as datetime
- Removed duplicate asteroid IDs — reduced 1596 to 1442 rows

Output: data/processed/asteroids_cleaned.csv

---

## 7. Feature Engineering

Performed in src/risk_score.py:

- month              : Numeric month from close_approach_date
- day_name           : Day of week (Monday … Sunday)
- velocity_category  : Low / Medium / High (thresholds: 0-15 / 15-25 / 25+ km/s)
- normalized_size     : average_diameter / max(average_diameter)
- normalized_speed    : relative_velocity_km_s / max(relative_velocity_km_s)
- normalized_distance : 1 − (miss_distance_km / max(miss_distance_km))
- hazardous_flag      : Boolean → integer (0 or 1)

---

## 8. Risk Score Formula

Each asteroid receives a score between 0 and 1:

  risk_score = (normalized_size     × 0.35)
             + (normalized_speed    × 0.25)
             + (normalized_distance × 0.30)
             + (hazardous_flag      × 0.10)

Weight rationale: size and miss distance together account for 65% because a large object
passing close to Earth represents the greatest physical threat. Speed adds kinetic-energy
context, and the NASA hazard flag provides an independent expert signal.

Risk levels are assigned by fixed thresholds:

  0.00 – 0.25  →  Low
  0.25 – 0.50  →  Medium
  0.50 – 0.75  →  High
  0.75 – 1.00  →  Critical

Note: Because max-normalisation is used, no asteroid simultaneously achieves the maximum
value in all three features. As a result scores are concentrated below 0.55 and the
Critical band is empty — this reflects the natural distribution of the data, not an
error in the formula.

---

## 9. Exploratory Data Analysis

See notebooks/asteroid_analysis.ipynb for the full EDA. Key questions answered:

General:
  - How many asteroids were observed in total?
  - How many are potentially hazardous?
  - What is the average approach distance and speed?
  - Which asteroid is the largest / closest / riskiest?

Time-based:
  - Which month had the most close approaches?
  - On which days of the week do risky approaches cluster?
  - Is there a seasonal trend in high-risk objects?

Risk-based:
  - How are asteroids distributed across risk levels?
  - Do hazardous asteroids have significantly higher velocities?
  - Does proximity always correlate with danger?
  - Is there a relationship between diameter and risk score?

---

## 10. Visualisations

All charts are saved to outputs/figures/.

  1_risk_distribution.png       : Count of asteroids per risk level
  2_diameter_vs_distance.png    : Scatter — diameter vs miss distance, coloured by risk
  3_velocity_vs_risk.png        : Scatter — velocity vs risk score
  4_monthly_density.png         : Bar chart — approaches per month
  5_top_10_risky_asteroids.png  : Horizontal bar — top 10 by risk score
  6_correlation_heatmap.png     : Pearson correlation matrix of numeric features

---

## 11. Key Insights

- 1442 unique asteroids made close approaches to Earth in 2025.
- 154 (10.7%) are flagged as potentially hazardous by NASA.
- Average approach distance: ~38 million km. Average velocity: ~14 km/s.
- Largest asteroid: 433 Eros (~35.9 km diameter).
- Closest approach: (2025 US6) at ~381 125 km — inside the Moon's orbit.
- Highest risk score: 0.513 — asteroid 488789 (2004 XK50).
- Most asteroids (58%) fall in the Low risk band; no asteroid reached Critical.
- Risk scores cluster between 0.15–0.35 due to max-normalisation.

---

## 12. How to Run the Project

Prerequisites:

  pip install -r requirements.txt

Create a .env file in the project root:

  NASA_API_KEY=your_api_key_here

Get a free key at https://api.nasa.gov/

Run the full pipeline:

  python main.py

This will:
  1. Fetch data from NASA (skipped if raw JSON already exists)
  2. Clean and save data/processed/asteroids_cleaned.csv
  3. Calculate risk scores and save data/processed/asteroids_final.csv
  4. Generate all plots into outputs/figures/
  5. Generate summary report at outputs/reports/summary_report.txt

Run individual steps:

  python src/fetch_data.py
  python src/clean_data.py
  python src/risk_score.py
  python src/visualize.py
  python src/generate_report.py

Open the notebook:

  jupyter notebook notebooks/asteroid_analysis.ipynb

---

## 13. Future Improvements

- Min-max normalisation instead of max normalisation — would spread scores across
  the full 0–1 range and populate the Critical category.
- Multi-year analysis — extend the date range to identify long-term trends.
- Interactive dashboard — replace static matplotlib charts with a Plotly / Dash app.
- Orbit classification — group asteroids by orbital type (Aten, Apollo, Amor).
- Automated alerts — email or Slack notification when a newly fetched asteroid
  exceeds a risk threshold.