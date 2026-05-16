from clean_data import clean_asteroid_data
import pandas as pd
import os,sys

def calculate_risk(df):
    # ---- Feature Engineering -----
    df["month"]=df["close_approach_date"].dt.month
    df["day_name"] = df["close_approach_date"].dt.day_name()

   # 0-15: Low, 15-25: Medium, 25+: High
    df["velocity_category"]=pd.cut(
        df["relative_velocity_km_s"],
        bins=(0,15,25,float("inf")),
        labels=("Low","Medium", "High")
        )
    
    # ------ Normalise ------

    df["normalized_size"]= df["average_diameter"] / df["average_diameter"].max()
    df["normalized_speed"]= df["relative_velocity_km_s"] / df["relative_velocity_km_s"].max()
    df["normalized_distance"]= 1 - (df["miss_distance_km"]  / df["miss_distance_km"].max())
    df["hazardous_flag"] = df["is_potentially_hazardous_asteroid"].astype(int)

    # ------- Risk Score ------

    df["risk_score"]=(
        df["normalized_size"] *0.35 +
        df["normalized_speed"] *0.25 +
        df["normalized_distance"] *0.30 +
        df["hazardous_flag"] *0.10
    )
  
   # ------ Risk Level --------
    df["risk_level"]= pd.cut(
        df["risk_score"],
        bins=(0,0.25,0.50,0.75,1.0),
        labels=("Low","Medium","High","Critical")
    )

    return df

if __name__=="__main__":
    df = clean_asteroid_data()
    if df is not None:
        df = calculate_risk(df)
        output_path = "data/processed/asteroids_final.csv"
        os.makedirs("data/processed", exist_ok=True)
        df.to_csv(output_path, index=False)
        print("\n--- Feature Engineering & Risk Scoring Complete ---")
        print(f"Final data saved to: {output_path}")
        print(df[["name", "risk_score", "risk_level"]].sort_values("risk_score", ascending=False).head(10))






    

