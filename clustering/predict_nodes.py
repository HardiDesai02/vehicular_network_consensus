import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# Load model and data
model = load_model("node_selection_model.h5")
df = pd.read_csv("clustered_vehicles.csv")

# Prepare input features (e.g., speed and x-position)
X = np.array(df[["Speed", "Position"]].apply(lambda x: [x[0], x[1][0]], axis=1).tolist())

# Predict suitability (you get float values between 0 and 1)
predictions = model.predict(X)

# Select nodes with prediction > 0.7 (threshold for selection)
selected_nodes = df[predictions.flatten() > 0.7]
selected_nodes["NodeID"] = selected_nodes["Vehicle_ID"]

# Save selected consensus node IDs
selected_nodes.to_csv("selected_nodes.csv", index=False)
print("✅ Selected nodes written to selected_nodes.csv")
