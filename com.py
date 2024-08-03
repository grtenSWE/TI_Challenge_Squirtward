from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
import warnings
from playsound import playsound
import speech_recognition as sr
from openai import OpenAI
import time

# Functions and classes for handling the response
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
                {"role": "system", "content": "You are handsome Squidward from Spongebob. You are feeling humorous and edgy today, and someone is flirting with you. Respond with a 1 if it's good and 0 otherwise, followed by a space and short message (spoken like Squidward) of why you think the flirting is good or not"},
                {"role": "user", "content": text}
            ]
        )
        bin_ans = int(completion.choices[0].message.content[0])
        txt_ans = completion.choices[0].message.content[1:]
        print(txt_ans + "\n")
        self.__text_to_speech(txt_ans)
        return bin_ans

    def __text_to_speech(self, txt_ans):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        with open("key.txt") as key_file:
            key = key_file.read()
        client = OpenAI(api_key=key)
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=txt_ans
        )
        response.stream_to_file("speech.mp3")
        playsound("speech.mp3")

def get_image(frame, bg, filepath, resize, transparency=1.0):
    try:
        IMG = Image.open(filepath).convert("RGBA")
        IMG = IMG.resize(resize)
        if transparency < 1.0:
            alpha = IMG.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(transparency)
            IMG.putalpha(alpha)
        image = ImageTk.PhotoImage(IMG)
        img_lbl = Label(frame, image=image, bg=bg)
        img_lbl.image = image
        return img_lbl
    except Exception as e:
        print(f"Error loading image: {e}")
        return Label(frame, text="Image not found", bg=bg, fg="red")

class GUI:
    def __init__(self, parent):
        self.response = Response()
        self.parent = parent
        self.MED_FONT = ("Helvetica", 65, "bold")
        self.MED_FONT1 = ("Helvetica", 36)
        self.MED_FONT2 = ("Helvetica", 36, "bold")
        self.SMALL_FONT = ("Helvetica", 26, "bold")
        self.SMALL_FONT2 = ("Helvetica", 15)
        self.SMALL_FONT3 = ("Helvetica", 18)
        self.SMALL_FONT4 = ("Helvetica", 15, "underline")
        self.SMALL_FONT5 = ("Helvetica", 15, "bold")
        self.TINY_FONT = ("Helvetica", 12)
        self.TINY_FONT2 = ("Helvetica", 12, "underline")

        self.main = Frame(parent, bg='black')
        self.main.pack(fill=BOTH, expand=True)

        self.on = Frame(self.main, bg='black')
        self.on.pack(fill=BOTH, expand=True)

        self.start_prompt = Label(self.on, text="Click Anywhere to Start", fg="white", bg="black", font=self.MED_FONT1)
        self.start_prompt.pack(expand=True)

        self.on.bind("<Button-1>", self.start_interface)
        self.start_prompt.bind("<Button-1>", self.start_interface)

    def start_interface(self, event=None):
        self.forget_screen(self.on)
        self.neutral = get_image(self.main, 'white', 'face_pics/Annoy_Squidward.jpg', (1200, 850))
        self.neutral.pack(expand=True, anchor=S)
        self.listening()

    def listening(self):
        self.listen_prompt = Label(self.main, text="listening...", fg="white", bg="black", font=self.MED_FONT2)
        self.listen_prompt.pack(expand=True, anchor=S)
        response = self.response.speech_to_text()

        self.forget_screen([self.neutral, self.listen_prompt])

        if response == 1:
            self.handsome()
        else:
            self.angry()

    def handsome(self):
        self.handsome_pic = get_image(self.main, 'white', 'face_pics/handsome_squidward.jpg', (1200, 850))
        self.handsome_pic.pack(expand=True, anchor=S)

    def angry(self):
        self.angry_pic = get_image(self.main, 'white', 'face_pics/angry_squidward.jpg', (1200, 850))
        self.angry_pic.pack(expand=True, anchor=S)

    @staticmethod
    def forget_screen(widgets):
        try:
            for wid in widgets:
                wid.pack_forget()
        except:
            widgets.pack_forget()

    @staticmethod
    def destroy_screen(widgets):
        try:
            for wid in widgets:
                wid.destroy()
        except:
            widgets.destroy()

# Main loop
root = Tk()
GUI(root)
root.title("SquirtWard Face")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.destroy())
root.mainloop()