from clean_data import clean_asteroid_data
import pandas as pd
import os

df = clean_asteroid_data()

if df is not None:
    # --- FEATURE ENGINEERING ---
   
    df['month'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    
    # 0-15: Low, 15-25: Medium, 25+: High
    df['velocity_category'] = pd.cut(df['velocity_km_s'], 
                                     bins=[0, 15, 25, float('inf')], 
                                     labels=['Low', 'Medium', 'High'])

    # --- CALCULATE RISK SCORE ---
    
    df["size_norm"] = df["avg_diameter_km"] / df["avg_diameter_km"].max()
    df["speed_norm"] = df["velocity_km_s"] / df["velocity_km_s"].max()
    df["distance_norm"] = 1 - (df["miss_distance_km"] / df["miss_distance_km"].max())
    
    #  (True -> 1, False -> 0)
    df["hazardous_flag"] = df["is_hazardous"].astype(int)

    df["risk_score"] = (
        df["size_norm"] * 0.35 +
        df["speed_norm"] * 0.25 +
        df["distance_norm"] * 0.30 +
        df["hazardous_flag"] * 0.10
    )
    
    # DEFINE RISK LEVEL
    df['risk_level'] = pd.cut(df['risk_score'], 
                              bins=[0, 0.25, 0.50, 0.75, 1.0], 
                              labels=['Low', 'Medium', 'High', 'Critical'])

    # SAVE DATA
    output_path = "data/processed/asteroids_final.csv"
    df.to_csv(output_path, index=False)
    
    print("\n--- Feature Engineering & Risk Scoring Complete ---")
    print(f"Final data saved to: {output_path}")
    

