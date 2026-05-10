import json
import os
import pandas as pd

def clean_asteroid_data(input_file="data/raw/nasa_neo_raw.json"):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return None

    with open(input_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    rows = []
    for date, asteroids in raw_data.items():
        for asteroid in asteroids:
            row = {
                "id": asteroid["id"],
                "name": asteroid["name"],
                "date": date,
                "min_diameter_km": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
                "max_diameter_km": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
                "is_hazardous": asteroid["is_potentially_hazardous_asteroid"],
                "velocity_km_s": float(asteroid["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"]),
                "miss_distance_km": float(asteroid["close_approach_data"][0]["miss_distance"]["kilometers"])
            }
            rows.append(row)

    df = pd.DataFrame(rows)

   
    print("\n--- Raw Data Overview ---")
    print(df.info())
    print("\nMissing values before cleaning:\n", df.isnull().sum())

    df['date'] = pd.to_datetime(df['date']) 
    df["avg_diameter_km"] = (df["min_diameter_km"] + df["max_diameter_km"]) /2
    df = df.drop_duplicates()

    
    print("\n--- Cleaning Complete ---")
    print(f"Final shape: {df.shape}")
    
    return df

def save_cleaned_data(df, filename="asteroids_cleaned.csv"):
    os.makedirs("data/processed", exist_ok=True)
    output_path = os.path.join("data/processed", filename)
    df.to_csv(output_path, index=False)
    print(f"\nSuccess! Cleaned data saved to: {output_path}")

if __name__ == "__main__":
    cleaned_df = clean_asteroid_data()
    if cleaned_df is not None:
        save_cleaned_data(cleaned_df)