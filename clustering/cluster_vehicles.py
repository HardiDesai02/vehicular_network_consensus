import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import ast  # To safely evaluate string tuples as real tuples

# Load data
df = pd.read_csv("sumo_simulation/vehicle_data.csv")

# Convert 'Position' column from string to tuple
df["Position"] = df["Position"].apply(ast.literal_eval)  # Converts "(x, y)" to (x, y)

# Extract numerical values
X = np.array(df.apply(lambda x: [x["Speed"], x["Position"][0]], axis=1).tolist())  # Use x[0] from tuple

# K-Means clustering
kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
df["Cluster"] = kmeans.labels_

# Save results
df.to_csv("clustering/clustered_vehicles.csv", index=False)

# Plot results
plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, cmap="rainbow")
plt.title("Vehicular Node Clustering")
plt.xlabel("Speed")
plt.ylabel("X Position")
plt.show()

