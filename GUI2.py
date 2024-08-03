from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
import threading
from data2 import Response

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
        threading.Thread(target=self.process_speech).start()

    def process_speech(self):
        response= self.response.speech_to_text()
        self.update_display(response)

    def update_display(self, response):
        self.forget_screen([self.neutral, self.listen_prompt])
        if response == 1:
            self.handsome()
        else:
            self.angry()
        # Introduce a slight delay to ensure the GUI updates before playing the audio
        #self.start_audio_thread, txt_ans
        threading.Thread(target=self.response.text_to_speech()).start()

    #def start_audio(self):
        #threading.Thread(target=self.response.text_to_speech, args=(txt_ans,)).start()

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
