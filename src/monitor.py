import random
from datetime import datetime
from tabulate import tabulate
from ai_model import AIModel

class SafetyMonitor:
       def __init__(self):
           self.log_file = "logs/safety_log.txt"
           self.thresholds = {
               "pressure": (900, 1100),  # hPa
               "oxygen": (19, 23),       # %
               "radiation": (0, 0.1)     # mSv/h
           }
           self.moderate_thresholds = {
               "pressure": (920, 1080),  # 5% margin from safe thresholds
               "oxygen": (19.5, 22.5),
               "radiation": (0, 0.08)
           }
           self.ai_model = AIModel()
           self.data_buffer = []  # Store data for AI training

       def get_safety_data(self):
           """Simulate collecting safety data."""
           data = {
               "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               "pressure": random.uniform(800, 1200),
               "oxygen": random.uniform(15, 25),
               "radiation": random.uniform(0, 0.2)
           }
           self.data_buffer.append(data)
           if len(self.data_buffer) >= 10:
               self.ai_model.train(self.data_buffer[-10:])  # Use last 10 points
           self.log_data(data)
           return data

       def log_data(self, data):
           """Log safety data to a file with anomaly status."""
           is_anomaly = self.ai_model.predict(data) if len(self.data_buffer) >= 10 else False
           with open(self.log_file, "a") as f:
               f.write(f"{data['timestamp']}, {data['pressure']:.2f}, {data['oxygen']:.2f}, {data['radiation']:.2f}, {is_anomaly}\n")

       def is_safe(self, data):
           """Check if parameters are within safe thresholds."""
           for param, (min_val, max_val) in self.thresholds.items():
               if not (min_val <= data[param] <= max_val):
                   return False
           return True

       def is_moderate(self, data):
           """Check if parameters are in moderate range or AI detects an anomaly."""
           if self.is_anomaly(data):
               return True
           for param, (min_val, max_val) in self.moderate_thresholds.items():
               if not (min_val <= data[param] <= max_val):
                   return True
           return False

       def is_anomaly(self, data):
           """Check if data is an anomaly using AI model."""
           if len(self.data_buffer) < 10:
               return False
           return self.ai_model.predict(data)

       def get_signal_status(self, data):
           """Determine signal status: red (unsafe), yellow (moderate/anomaly), green (safe)."""
           if not self.is_safe(data):
               return "red"
           elif self.is_moderate(data):
               return "yellow"
           return "green"

       def display_data(self, data):
           """Display safety data in a table with anomaly and signal status."""
           is_anomaly = self.is_anomaly(data)
           signal_status = self.get_signal_status(data)
           table = [[data["timestamp"], f"{data['pressure']:.2f}", f"{data['oxygen']:.2f}", f"{data['radiation']:.2f}", "Anomaly" if is_anomaly else "Normal", signal_status.capitalize()]]
           headers = ["Timestamp", "Pressure (hPa)", "Oxygen (%)", "Radiation (mSv/h)", "AI Status", "Signal"]
           return tabulate(table, headers, tablefmt="grid")