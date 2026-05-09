from clean_data import clean_asteroid_data

df=clean_asteroid_data()

if df is not None:

    # Normalization
    df["size_norm"]=df["avg_diameter_km"]/df["avg_diameter_km"].max()
    df["speed_norm"]=df["velocity_km_s"]/df["velocity_km_s"].max()
    df["distance_norm"]=1- (df["miss_distance_km"]/df["miss_distance_km"].max())

    df["hazardous_flag"]=df["is_hazardous"].astype(int)

    # Calculate risk score 
    df["risk_score"]= (
    df["size_norm"]*0.35+
    df["speed_norm"]*0.25+
    df["distance_norm"]*0.30+
    df["hazardous_flag"]*0.10
)

