# parse_vehicle_data.py
import pandas as pd
import json

try:
    # Read the CSV file
    df = pd.read_csv('clustered_vehicles.csv')
except FileNotFoundError:
    print("Error: clustered_vehicles.csv not found.")
    exit(1)

# Convert Position tuple strings to structured format
df['Position_X'] = df['Position'].apply(lambda x: float(x.strip('()').split(',')[0]))
df['Position_Y'] = df['Position'].apply(lambda x: float(x.strip('()').split(',')[1]))

# Group by Vehicle_ID and format data
vehicle_data = []
for vehicle_id, group in df.groupby('Vehicle_ID'):
    records = group[['Speed', 'Position_X', 'Position_Y', 'Cluster']].to_dict('records')
    vehicle_data.append({
        'VehicleID': vehicle_id,
        'Records': records
    })

# Save to JSON
with open('vehicle_data.json', 'w') as f:
    json.dump(vehicle_data, f, indent=4)

print(f"Parsed {len(vehicle_data)} vehicles to vehicle_data.json")
