import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import ast
import os

# Load data
df = pd.read_csv("data/vehicle_data.csv")
df["Position"] = df["Position"].apply(ast.literal_eval)

# Feature vector: [Speed, X-position]
X = np.array(df.apply(lambda row: [row["Speed"], row["Position"][0]], axis=1).tolist())

# Clustering
kmeans = KMeans(n_clusters=5, random_state=0)
df["Cluster"] = kmeans.fit_predict(X)

# Save results
os.makedirs("results/plots", exist_ok=True)
df.to_csv("data/clustered_vehicles.csv", index=False)

# Plot
plt.scatter(X[:, 0], X[:, 1], c=df["Cluster"], cmap="rainbow")
plt.xlabel("Speed")
plt.ylabel("X Position")
plt.title("Vehicle Clusters")
plt.savefig("results/plots/clusters.png")
plt.show()
