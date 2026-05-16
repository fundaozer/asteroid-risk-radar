import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import os


# VISUALIZE THE DATA

def load_data():
    file_path = "data/processed/asteroids_final.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"Error: {file_path}")
   
def  save_plot(filename):
    output_dir = "outputs/figures"
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)
    plt.savefig(full_path, bbox_inches='tight', dpi=300)
    plt.close()

def plot_risk_distribution(df):
    plt.figure(figsize=(8,6))
    sns.countplot(
        data=df,
        x='risk_level',
        order=['Low','Medium','High','Critical'],
        palette='magma'
    )
    plt.title('Distribution of Asteroids by Risk Level', fontweight='bold')
    plt.xlabel('Risk Level')
    plt.ylabel('Asteroid Count')
    save_plot('1_risk_distribution.png')



def plot_diameter_vs_distance(df):
    plt.figure(figsize=(8,6))
    sns.scatterplot(
        data=df,
        x='average_diameter',
        y='miss_distance_km',
        hue='risk_level',
        hue_order=['Low','Medium','High','Critical'],
        palette='viridis'
    )
    plt.title('Asteroid Diameter vs. Miss Distance', fontweight='bold')
    plt.xlabel('Asteroid Diameter (km)')
    plt.ylabel('Miss Distance (km)')
    plt.legend(title='Risk Level')
    save_plot('2_diameter_vs_distance.png')

def plot_velocity_vs_risk(df):
    plt.figure(figsize=(8,6))
    sns.scatterplot(
        data=df,
        x='relative_velocity_km_s',
        y='risk_score',
        hue='risk_level',
        hue_order=['Low','Medium','High','Critical'],
        palette='viridis'
    )
    plt.title('Asteroid Velocity vs. Risk Score', fontweight='bold')
    plt.xlabel('Velocity (km/s)')
    plt.ylabel('Risk Score')
    plt.legend(title='Risk Level')
    save_plot('3_velocity_vs_risk.png')

def plot_monthly_density(df):
    plt.figure(figsize=(10, 5))
    
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    if 'month_name' not in df.columns:
        df['month_name'] = df['month'].map(month_map)
    
    monthly_counts = df['month_name'].value_counts().reindex(month_order).fillna(0)
    
    sns.barplot(
        x=monthly_counts.index, 
        y=monthly_counts.values, 
        hue=monthly_counts.index, 
        palette='Blues_d', 
        legend=False
    )
    
    plt.title('Asteroid Approach Density by Month', fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Number of Approaches')
    plt.xticks(rotation=45) 
    save_plot('4_monthly_density.png')

def plot_top_10_risky(df):
    plt.figure(figsize=(10, 6))
    
    top_10 = df.sort_values(by='risk_score', ascending=False).head(10)
    
    sns.barplot(data=top_10, x='risk_score', y='name', palette='flare')
    
    plt.title('Top 10 Most Risky Asteroids',  fontweight='bold')
    plt.xlabel('Risk Score')
    plt.ylabel('Asteroid Name')
    save_plot('5_top_10_risky_asteroids.png')

def plot_correlation_heatmap(df):
    plt.figure(figsize=(8, 6))
    
    numeric_cols = ['average_diameter', 'relative_velocity_km_s', 'miss_distance_km', 'risk_score']
    corr_matrix = df[numeric_cols].corr()
    
    # Heatmap
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Matrix of Asteroid Features', fontweight='bold')
    save_plot('6_correlation_heatmap.png')

if __name__ == "__main__":
    try:
        df= load_data()
        
        plot_risk_distribution(df)
        plot_diameter_vs_distance(df)
        plot_velocity_vs_risk(df)
        plot_monthly_density(df)
        plot_top_10_risky(df)
        plot_correlation_heatmap(df)
        
        print("=== ALL PLOTS WEre SAVED ===")
    except Exception as e:
        print(f"An error: {e}")