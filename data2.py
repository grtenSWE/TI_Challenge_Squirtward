import warnings
from playsound import playsound
import speech_recognition as sr
from openai import OpenAI

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
            response = "I got no rizz"
        print(response + "\n")
        return self.__check_flirting(response)

    def __check_flirting(self, text):
        with open("key.txt") as key_file:
            key = key_file.read()
        client = OpenAI(api_key=key)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Squidward from Spongebob. You are feeling humorous and edgy today, and someone is flirting with you. Respond with a 1 if it's good and 0 otherwise, followed by a space and short message (spoken like Squidward would) of why you think the flirting is good or not"},
                {"role": "user", "content": text}
            ]
        )
        bin_ans = int(completion.choices[0].message.content[0])
        txt_ans = completion.choices[0].message.content[1:]
        self.txt_ans = txt_ans
        print(txt_ans + "\n")
        return bin_ans

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
        playsound("speech.mp3")
