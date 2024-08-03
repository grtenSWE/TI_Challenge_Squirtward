import warnings
from playsound import playsound
import speech_recognition as sr
from openai import OpenAI
import serial 
import time

class Response:
    def speech_to_text(self):
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=15, phrase_time_limit=15)
        try:
            response = r.recognize_google(audio)
        except sr.RequestError:
            response = "API unavailable"
        except sr.UnknownValueError:
            response = "I got no rizz and i thought of nothing"
        print(response + "\n")
        return self.__check_flirting(response)

    def __check_flirting(self, text):
        with open("key.txt") as key_file:
            key = key_file.read()
        client = OpenAI(api_key=key)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Squidward from Spongebob. You are feeling humorous, edgy and have a big appetite for sexual innuendoes (especially about tentacles and your nose shape and size), and someone is flirting with you. Respond with a 1 if it's good and 0 otherwise, followed by a space and short message (spoken like Squidward would). The message would be how you feel about the flirting. You can throw insult back at them if you really hate the response or flirtback if you love it (do it like how squidward might)"},
                {"role": "user", "content": text}
            ]
        )
        self.bin_ans = int(completion.choices[0].message.content[0])
        self.txt_ans = completion.choices[0].message.content[1:]
       
        print(self.txt_ans + "\n")
        return self.bin_ans

    def text_to_speech(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        with open("key.txt") as key_file:
            key = key_file.read()
        client = OpenAI(api_key=key)
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=self.txt_ans
        )
        response.stream_to_file("speech.mp3")

        if self.txt_ans == 1: #<---------- calls the serialcomm function to send signal to arduino
            serialComm()

        playsound("speech.mp3")
        

#function to tell the arduino to do stuff
def serialComm():
   
    # Open serial connection to Arduino (replace 'COMS' with your actual port)
    arduino = serial.Serial("COM5", 9600)
    time.sleep(2)  # Wait for the connection to be established

    print("1")
    arduino.write(b'1')
 

    arduino.close()