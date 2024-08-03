from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
import os
import data
import time


# functions
def get_image(frame, bg, filepath, resize, transparency=1.0):
    """returns a working image label with optional transparency"""
    IMG = Image.open(filepath).convert("RGBA")
    IMG = IMG.resize(resize)
    
    # Apply transparency
    if transparency < 1.0:
        alpha = IMG.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(transparency)
        IMG.putalpha(alpha)
    
    image = ImageTk.PhotoImage(IMG)
    img_lbl = Label(frame, image=image, bg=bg)
    img_lbl.image = image
    return img_lbl


# main GUI class
class GUI:
    """this class runs the interface"""
    def __init__(self, parent):
        self.response = data.Response()

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

        # Initialize the full-screen black background
        self.main = Frame(parent, bg='black')
        self.main.pack(fill=BOTH, expand=True)

        #self.on = Frame(self.main, bg='black')
        #self.on.pack(fill=BOTH, expand=True)

        # Add the "Click Anywhere to Start" label
        #self.start_prompt = Label(self.on, text="Click Anywhere to Start", fg="white", bg="black", font=self.MED_FONT1)
        #self.start_prompt.pack(expand=True)

        self.neutral = get_image(self.main, 'white', 'face_pics/Annoy_Squidward.jpg', (1200, 850))
        self.neutral.pack(expand=True,anchor=S)
        self.listen_prompt = Label(self.main, text="click and rizz me up...", fg="white", bg="black", font=self.MED_FONT2)
        self.listen_prompt.pack(expand=True,anchor=N)

        self.neutral.bind("<Button-1>", self.start_interface)

    def start_interface(self, event=None):
        self.listening()


    def listening(self):

        response = self.response.speech_to_text()

        self.forget_screen([self.neutral,self.listen_prompt])

        if response == 1:
            self.handsome()

        else:
            self.angry()
            
        self.response.text_to_speech() 

    def handsome(self):
        self.handsome_pic = get_image(self.main, 'white', 'face_pics/handsome_squidward.jpg', (1200, 850))
        self.handsome_pic.pack(expand=True,anchor=S)


    def angry(self):
        self.angry_pic = get_image(self.main, 'white', 'face_pics/angry_squidward.jpg', (1200, 850))
        self.angry_pic.pack(expand=True,anchor=S)


    @staticmethod
    def forget_screen(widgets):
        """forgets all the widgets on the window given the list of widgets"""
        try:
            for wid in widgets:
                wid.pack_forget()
        except:
            widgets.pack_forget()


    @staticmethod
    def destroy_screen(widgets):
        """destroys all the widgets on the window given the list of widgets"""
        try:
            for wid in widgets:
                wid.destroy()
        except:
            widgets.destroy()


 


# mainloop
root = Tk()
GUI(root)
root.title("SquirtWard Face")
root.attributes("-fullscreen", True)  # Make the window full-screen
root.bind("<Escape>", lambda e: root.destroy())  # Pressing Escape will exit the full-screen mode
root.mainloop()
