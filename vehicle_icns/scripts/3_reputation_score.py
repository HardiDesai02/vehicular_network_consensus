import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load datasets
df = pd.read_csv("data/clustered_vehicles.csv")
df["Time"] = df.index
df["T_init"] = df.groupby("Vehicle_ID")["Time"].transform("min")
df["AoN"] = df["Time"] - df["T_init"]
sob_map = pd.Series(np.random.uniform(0.5, 1.0, size=df["Vehicle_ID"].nunique()), index=df["Vehicle_ID"].unique())
df["SoB"] = df["Vehicle_ID"].map(sob_map)

stability_df = pd.read_csv("results/stability.csv")
SoN_avg_per_vehicle = stability_df.groupby("Vehicle_ID")["SoN"].mean().rename("SoN")
df = df.merge(SoN_avg_per_vehicle, on="Vehicle_ID", how="left")

# Normalize by average
AoN_avg = df["AoN"].mean()
SoN_avg = df["SoN"].mean()
SoB_avg = df["SoB"].mean()

# Reputation score formula
df["Reputation"] = (df["AoN"] / AoN_avg) + (df["SoN"] / SoN_avg) + (df["SoB"] / SoB_avg)

# Save results
df[["Vehicle_ID", "Cluster", "AoN", "SoN", "SoB", "Reputation"]].drop_duplicates().to_csv("results/reputation_scores.csv", index=False)

# Plot
plt.figure()
df["Reputation"].hist(bins=20, color='skyblue')
plt.title("Distribution of Vehicle Reputation Scores")
plt.xlabel("Reputation")
plt.ylabel("Vehicle Count")
plt.savefig("results/plots/reputation_distribution.png")
plt.show()
