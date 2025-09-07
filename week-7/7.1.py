import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# --- CONFIGURATION ---
DATA_FILE = "dht22_data.csv"

# Load the data without headers and assign proper column names
df = pd.read_csv(DATA_FILE, header=None)
df.columns = ['timestamp', 'humidity', 'temperature']

# Convert columns to numeric (in case they were read as strings)
df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')

# Remove any rows with invalid data
df = df.dropna()

# Set column names for analysis
TEMPERATURE_COL = 'temperature'
HUMIDITY_COL = 'humidity'

# Outlier Filtering thresholds
min_temp_filter = -40
max_temp_filter = 80

# --- FUNCTION TO RUN THE ANALYSIS ---
def run_analysis(df, scenario_name):

    print(f"\n--- Analyzing Scenario: {scenario_name} ---")
    print(f"Number of data points: {len(df)}")

    # Prepare the data for sklearn
    X = df[TEMPERATURE_COL].values.reshape(-1, 1)
    y = df[HUMIDITY_COL].values

    # Create and train the Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    # Get model parameters (slope and intercept)
    slope = model.coef_[0]
    intercept = model.intercept_
    print(f"Linear Model: Humidity = {slope:.4f} * Temperature + {intercept:.4f}")
    print(f"R² Score (goodness of fit): {model.score(X, y):.4f}")

    # Create 100 test temperature points between the min and max of the training data
    x_range = np.linspace(X.min(), X.max(), 100)
    # Predict humidity for these test points
    y_range = model.predict(x_range.reshape(-1, 1))

    # Create the interactive plot
    fig = px.scatter(df, x=TEMPERATURE_COL, y=HUMIDITY_COL,
                     title=f'{scenario_name}<br>Humidity vs Temperature',
                     opacity=0.6, 
                     labels={'temperature': 'Temperature (°C)', 'humidity': 'Humidity (%)'})
    
    # Add the regression line to the plot
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Trend', line=dict(color='red')))
    
    # Show the plot in your browser
    fig.show()

    return model, fig

# --- MAIN PROGRAM ---
# Display basic info about the original data
print("\nOriginal Data Info:")
print(df[[TEMPERATURE_COL, HUMIDITY_COL]].describe())

# SCENARIO 1: Original Data (with all outliers)
model_original, fig_original = run_analysis(df, "Scenario 1 - Original Data")

# SCENARIO 2: Filtered Data (remove obvious outliers)
print("\nApplying initial outlier filter...")
# Adjust these values based on your data distribution
min_temp_filter = 15
max_temp_filter = 30

df_filtered1 = df[(df[TEMPERATURE_COL] >= min_temp_filter) & (df[TEMPERATURE_COL] <= max_temp_filter)]
model_filtered1, fig_filtered1 = run_analysis(df_filtered1, f"Scenario 2 - Filtered {min_temp_filter}°C to {max_temp_filter}°C")

# SCENARIO 3: Filtered Data More Aggressively
print("\nApplying more aggressive filter...")
# Adjust these values based on your data distribution
min_temp_filter_aggressive = 18
max_temp_filter_aggressive = 25

df_filtered2 = df[(df[TEMPERATURE_COL] >= min_temp_filter_aggressive) & (df[TEMPERATURE_COL] <= max_temp_filter_aggressive)]
model_filtered2, fig_filtered2 = run_analysis(df_filtered2, f"Scenario 3 - Filtered {min_temp_filter_aggressive}°C to {max_temp_filter_aggressive}°C")
