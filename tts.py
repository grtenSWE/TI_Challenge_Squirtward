from pathlib import Path
from openai import OpenAI
import warnings
from playsound import playsound


# Ignore DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)


with open("key.txt") as key_file:
        key = key_file.read()
    
client = OpenAI(api_key = key)

response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="Today is a wonderful day to build something people love! i like ronaldo"
)

response.stream_to_file("speech.mp3")
playsound("speech.mp3")