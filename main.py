"""
Asteroid Risk Radar - Main Pipeline
Run the full project with a single command:
  python main.py

Steps:
  1. Fetch asteroid data from NASA NeoWs API  (src/fetch_data.py)
  2. Clean and structure the raw JSON         (src/clean_data.py)
  3. Compute risk scores and feature engineer (src/risk_score.py)
  4. Generate visualisations                  (src/visualize.py)
  5. Generate summary report                  (src/generate_report.py)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from fetch_data      import fetch_asteroids, save_raw_data
from clean_data      import clean_asteroid_data, save_cleaned_data
from risk_score      import calculate_risk
from visualize       import (
    load_data,
    plot_risk_distribution,
    plot_diameter_vs_distance,
    plot_velocity_vs_risk,
    plot_monthly_density,
    plot_top_10_risky,
    plot_correlation_heatmap,
)
from generate_report import generate_summary_report

# --- Configuration ---
RAW_FILE   = "data/raw/nasa_neo_raw.json"
FINAL_CSV  = "data/processed/asteroids_final.csv"
START_DATE = "2025-01-01"
END_DATE   = "2025-12-31"


def main():

    # --- Step 1: Fetch data from NASA API ---
    print("\n" + "=" * 50)
    print("STEP 1: Fetching data from NASA API")
    print("=" * 50)

    if os.path.exists(RAW_FILE):
        # Skip fetching if raw data already exists
        print(f"Raw data already exists at '{RAW_FILE}', skipping fetch.")
    else:
        data = fetch_asteroids(START_DATE, END_DATE)
        if not data:
            print("No data fetched. Exiting.")
            return
        save_raw_data(data)

    # --- Step 2: Clean raw JSON and convert to DataFrame ---
    print("\n" + "=" * 50)
    print("STEP 2: Cleaning data")
    print("=" * 50)

    df = clean_asteroid_data(RAW_FILE)
    if df is None:
        print("Data cleaning failed. Exiting.")
        return
    save_cleaned_data(df)

    # --- Step 3: Feature engineering and risk scoring ---
    print("\n" + "=" * 50)
    print("STEP 3: Calculating risk scores")
    print("=" * 50)

    df = calculate_risk(df)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(FINAL_CSV, index=False)
    print(f"Final dataset saved -> {FINAL_CSV}")
    print(f"Total asteroids    : {len(df)}")
    print(f"Risk level breakdown:\n{df['risk_level'].value_counts().to_string()}")

    # --- Step 4: Generate and save all visualisations ---
    print("\n" + "=" * 50)
    print("STEP 4: Generating visualisations")
    print("=" * 50)

    # Reload from CSV to ensure consistent dtypes for plotting
    df = load_data()
    plot_risk_distribution(df)
    plot_diameter_vs_distance(df)
    plot_velocity_vs_risk(df)
    plot_monthly_density(df)
    plot_top_10_risky(df)
    plot_correlation_heatmap(df)
    print("All plots saved -> outputs/figures/")

    # --- Step 5: Generate summary report ---
    print("\n" + "=" * 50)
    print("STEP 5: Generating summary report")
    print("=" * 50)

    generate_summary_report(df)

    print("\n" + "=" * 50)
    print("Pipeline complete.")
    print("=" * 50)


if __name__ == "__main__":
    main()