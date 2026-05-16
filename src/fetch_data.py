from dotenv import load_dotenv
import pandas as pd, json,os ,time
from datetime import datetime,timedelta
import requests 

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
API_KEY=os.getenv("NASA_API_KEY")

def fetch_asteroids(start_date,end_date):
    url = "https://api.nasa.gov/neo/rest/v1/feed"
    all_asteroids = {}

    current_date=datetime.strptime(start_date, "%Y-%m-%d")
    final_date=datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= final_date:

        next_date=current_date+timedelta(days=6)

        if next_date > final_date:
            next_date=final_date

        params = {
            "start_date": current_date.strftime("%Y-%m-%d"),
            "end_date": next_date.strftime("%Y-%m-%d"),
            "api_key": API_KEY
        }

        print(f"Fetching data: {params['start_date']} - {params['end_date']}")
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data=response.json()

            if "near_earth_objects" in data:
                all_asteroids.update(data["near_earth_objects"])
            
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break 

        current_date = next_date + timedelta(days=1)
        time.sleep(1)
        
    return all_asteroids

def save_raw_data(data, filename="nasa_neo_raw.json"):

    if not data:
        print("No data to save.")
        return
    
    os.makedirs("data/raw", exist_ok=True)
    file_path = os.path.join("data/raw", filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Data successfully saved for {len(data)} days.")
    print(f"File location: {os.path.abspath(file_path)}")

if __name__ == "__main__":
   
    start_date = "2025-01-01"
    end_date = "2025-12-31" 
    
    asteroid_results = fetch_asteroids(start_date, end_date)
    save_raw_data(asteroid_results)

    
    
    