from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
import numpy as np
import ast  # To convert string tuples into numeric values
from tensorflow.keras.utils import to_categorical

# Load dataset
df = pd.read_csv("clustering/clustered_vehicles.csv")

# Convert Position column from string to tuple
df["Position"] = df["Position"].apply(ast.literal_eval)  # Converts "(x, y)" to (x, y)

# Extract features and labels
X = np.array(df.apply(lambda x: [x["Speed"], x["Position"][0]], axis=1).tolist())  # Using only X coordinate
y = df["Cluster"].values  # Labels (cluster IDs)

# Convert labels to categorical if needed
num_classes = len(df["Cluster"].unique())
y_categorical = to_categorical(y, num_classes)  # Convert integer labels to one-hot encoding

# Define neural network model
model = Sequential([
    Dense(16, activation='relu', input_shape=(2,)),
    Dense(8, activation='relu'),
    Dense(num_classes, activation='softmax')  # Multi-class classification output
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X, y_categorical, epochs=50, batch_size=10)

# Save the model
model.save("clustering/node_selection_model.h5")

