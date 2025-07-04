from tts import TTS

class AlertSystem:
       def __init__(self):
           self.tts = TTS()

       def trigger_alert(self, data, is_anomaly=False, signal_status="red"):
           """Trigger a visual and voice alert for unsafe conditions or AI-detected anomalies."""
           if is_anomaly:
               print("ALERT: AI detected an anomaly in safety parameters!")
               alert_message = f"Alert: Anomaly detected in safety parameters. Signal: {signal_status}."
           else:
               print(f"ALERT: Unsafe conditions detected! Signal: {signal_status}")
               alert_message = f"Alert: Unsafe conditions detected. Signal: {signal_status}."
           
           for param, value in data.items():
               if param != "timestamp":
                   print(f"{param.capitalize()}: {value:.2f}")
                   alert_message += f" {param.capitalize()}: {value:.2f}."
           
           self.tts.speak(alert_message)