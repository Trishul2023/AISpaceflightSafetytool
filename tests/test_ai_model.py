import unittest
from src.ai_model import AIModel

class TestAIModel(unittest.TestCase):
       def setUp(self):
           self.ai_model = AIModel()
           self.training_data = [
               {"pressure": 1000, "oxygen": 21, "radiation": 0.05},
               {"pressure": 1010, "oxygen": 20, "radiation": 0.06},
               {"pressure": 990, "oxygen": 22, "radiation": 0.04},
               {"pressure": 1200, "oxygen": 15, "radiation": 0.2}  # Outlier
           ]
           self.ai_model.train(self.training_data)

       def test_predict_anomaly(self):
           normal_data = {"pressure": 1000, "oxygen": 21, "radiation": 0.05}
           anomaly_data = {"pressure": 1200, "oxygen": 15, "radiation": 0.2}
           self.assertFalse(self.ai_model.predict(normal_data))
           self.assertTrue(self.ai_model.predict(anomaly_data))

if __name__ == "__main__":
       unittest.main()