from sklearn.ensemble import IsolationForest
import numpy as np

class AIModel:
       def __init__(self):
           self.model = IsolationForest(contamination=0.1, random_state=42)

       def train(self, data):
           """Train the Isolation Forest model on safety data."""
           # Convert data to numpy array (pressure, oxygen, radiation)
           X = np.array([[d["pressure"], d["oxygen"], d["radiation"]] for d in data])
           self.model.fit(X)

       def predict(self, data_point):
           """Predict if a data point is an anomaly."""
           X = np.array([[data_point["pressure"], data_point["oxygen"], data_point["radiation"]]])
           prediction = self.model.predict(X)
           return prediction[0] == -1  # -1 indicates anomaly