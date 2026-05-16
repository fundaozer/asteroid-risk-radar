import os
import pandas as pd
from datetime import datetime
 
def generate_summary_report(df, output_path="outputs/reports/summary_report.txt"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
 
    hazardous_count = int(df["is_potentially_hazardous_asteroid"].sum())
    total = len(df)
    riskiest = df.loc[df["risk_score"].idxmax()]
    closest  = df.loc[df["miss_distance_km"].idxmin()]
    biggest  = df.loc[df["average_diameter"].idxmax()]
    busiest_month = df["month"].value_counts().idxmax()
    month_names = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
                   7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
    risk_dist = df["risk_level"].value_counts().reindex(["Low","Medium","High","Critical"]).fillna(0).astype(int)
 
    lines = [
        "=" * 55,
        "         ASTEROID RISK RADAR — SUMMARY REPORT",
        f"         Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 55,
        "",
        "GENERAL STATISTICS",
        "-" * 55,
        f"  Total asteroids analysed   : {total}",
        f"  Potentially hazardous      : {hazardous_count} ({hazardous_count/total*100:.1f}%)",
        f"  Average approach distance  : {df['miss_distance_km'].mean():>15,.0f} km",
        f"  Average relative velocity  : {df['relative_velocity_km_s'].mean():>10.2f} km/s",
        "",
        "RISK LEVEL DISTRIBUTION",
        "-" * 55,
    ]
    for level, count in risk_dist.items():
        bar = "█" * int(count / total * 40)
        lines.append(f"  {level:<10} {count:>5}  {bar}")
 
    lines += [
        "",
        "NOTABLE ASTEROIDS",
        "-" * 55,
        f"  Highest risk score : {riskiest['name']}",
        f"                       Score {riskiest['risk_score']:.4f}  |  Level: {riskiest['risk_level']}",
        f"  Closest approach   : {closest['name']}",
        f"                       {closest['miss_distance_km']:,.0f} km  |  Date: {str(closest['close_approach_date'])[:10]}",
        f"  Largest diameter   : {biggest['name']}",
        f"                       {biggest['average_diameter']:.4f} km avg diameter",
        "",
        "TIME ANALYSIS",
        "-" * 55,
        f"  Busiest month      : {month_names.get(busiest_month, busiest_month)}",
        f"  Date range         : {str(df['close_approach_date'].min())[:10]} → {str(df['close_approach_date'].max())[:10]}",
        "",
        "=" * 55,
    ]
 
    report_text = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)
 
    print(report_text)
    print(f"\nReport saved → {output_path}")
 
if __name__ == "__main__":
    df = pd.read_csv("data/processed/asteroids_final.csv", parse_dates=["close_approach_date"])
    generate_summary_report(df)