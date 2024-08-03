from openai import OpenAI
import speech_recognition as sr 
#  Run pip install pyAudio 
# pip install SpeechRecognition
import warnings
from playsound import playsound
import serial 
import time


class Response:

    def speech_to_text(self): 
        # When click to start, start recognising microphone
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source: 
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=15, phrase_time_limit=15)
    
        try:
            # Recognize speech using Google Web Speech API
            response = r.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response = "API unavailable"
        except sr.UnknownValueError:
            # Speech was unintelligible
            response = "I got no rizz"

        print(response + "\n")
        self.__check_flirting(response) 


    def __check_flirting(self,text):
        with open("key.txt") as key_file:
            key = key_file.read()
        
        client = OpenAI(api_key = key)

        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are handsome Squidward from Spongebob. You are feeling humourous and edgy today, and someone is flirting with you. Respond with a 1 if it's good and 0 otherwise, followed by a space and short message (spoken like squidward) of why you think the flirting is good or not"},
            {"role": "user", "content": text}
        ]
        )
        bin_ans = completion.choices[0].message.content[0]
        txt_ans = completion.choices[0].message.content[1:]
        print(txt_ans + "\n")
        self.__text_to_speech(txt_ans)

        return bin_ans


    def __text_to_speech(self,txt_ans):
        # Ignore DeprecationWarning
        warnings.filterwarnings("ignore", category=DeprecationWarning)


        with open("key.txt") as key_file:
                key = key_file.read()
            
        client = OpenAI(api_key = key)

        response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=txt_ans
        )

        response.stream_to_file("speech.mp3")
        playsound("speech.mp3")


def serialComm():
   
    # Open serial connection to Arduino (replace 'COMS' with your actual port)
    arduino = serial.Serial("COM5", 9600)
    time.sleep(2)  # Wait for the connection to be established

    TorF = input("True or False? ")

    if TorF == "True":
        print("k dewd")
        arduino.write(b'T')
    elif TorF == "False":
        print("oh okay")
        arduino.write(b'F')

    arduino.close()


