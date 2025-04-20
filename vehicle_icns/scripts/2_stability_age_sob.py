import pandas as pd
import numpy as np
import os

df = pd.read_csv("data/clustered_vehicles.csv")
df["Time"] = df.index

# AoN
first_seen = df.groupby("Vehicle_ID")["Time"].min().rename("T_init")
df = df.merge(first_seen, on="Vehicle_ID")
df["AoN"] = df["Time"] - df["T_init"]

# Simulated SoB per vehicle
unique_vehicles = df["Vehicle_ID"].unique()
sob_values = pd.Series(np.random.uniform(0.5, 1.0, size=len(unique_vehicles)), index=unique_vehicles)
df["SoB"] = df["Vehicle_ID"].map(sob_values)

# Stability per cluster
vehicle_movements = {}
for _, row in df.iterrows():
    vid, time, cluster = row["Vehicle_ID"], row["Time"], row["Cluster"]
    if vid not in vehicle_movements:
        vehicle_movements[vid] = []
    if not vehicle_movements[vid] or vehicle_movements[vid][-1]["cluster"] != cluster:
        vehicle_movements[vid].append({"cluster": cluster, "entry_time": time})

vehicle_stability = []
for vid, visits in vehicle_movements.items():
    for i in range(len(visits)):
        entry = visits[i]["entry_time"]
        exit = visits[i + 1]["entry_time"] if i + 1 < len(visits) else df["Time"].max()
        vehicle_stability.append({"Vehicle_ID": vid, "Cluster": visits[i]["cluster"], "SoN": exit - entry})

stability_df = pd.DataFrame(vehicle_stability)
stability_df.to_csv("results/stability.csv", index=False)
