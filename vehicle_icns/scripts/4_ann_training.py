import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
import joblib

df = pd.read_csv("results/reputation_scores.csv")
features = df[["AoN", "SoN", "SoB"]]
target = df["Reputation"]

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# ANN model
model = MLPRegressor(hidden_layer_sizes=(16, 8), max_iter=1000, random_state=0)
model.fit(X_train, y_train)

# Print both training and testing accuracy
train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)

print("Training Accuracy (R²):", train_accuracy)
print("Testing Accuracy (R²):", test_accuracy)

# Save model
joblib.dump(model, "results/ann_model.pkl")
