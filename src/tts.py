import pyttsx3

class TTS:
       def __init__(self):
           self.engine = pyttsx3.init()
           self.set_female_voice()
           self.engine.setProperty("rate", 150)  # Speech speed

       def set_female_voice(self):
           """Select a female voice if available."""
           voices = self.engine.getProperty("voices")
           for voice in voices:
               if "female" in voice.name.lower() or any(name in voice.name.lower() for name in ["zira", "hazel", "eva"]):
                   self.engine.setProperty("voice", voice.id)
                   return
           print("Warning: No female voice found, using default voice.")

       def speak(self, text):
           """Speak the given text."""
           self.engine.say(text)
           self.engine.runAndWait()