from tkinter import *
from PIL import Image, ImageTk, ImageEnhance
import os
import data


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

        self.on = Frame(self.main, bg='black')
        self.on.pack(fill=BOTH, expand=True)

        # Add the "Click Anywhere to Start" label
        self.start_prompt = Label(self.on, text="Click Anywhere to Start", fg="white", bg="black", font=self.MED_FONT1)
        self.start_prompt.pack(expand=True)

        # Bind the click event to start the main interface
        self.on.bind("<Button-1>", self.start_interface)
        self.start_prompt.bind("<Button-1>", self.start_interface)

    def start_interface(self, event=None):
        # Remove the label
        self.forget_screen(self.on)
        bg = get_image(self.main, 'white', 'face_pics/Annoy_Squidward.jpg', (1200, 850))
        bg.pack(expand=True,anchor=S)
        self.face()


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

    def face(self):
        self.listen_prompt = Label(self.main, text="listening...", fg="white", bg="black", font=self.MED_FONT2)
        self.listen_prompt.pack(expand=True,anchor=S)
        print("yes")
        self.response.speech_to_text()



        
        


# mainloop
root = Tk()
GUI(root)
root.title("SquirtWard Face")
root.attributes("-fullscreen", True)  # Make the window full-screen
root.bind("<Escape>", lambda e: root.destroy())  # Pressing Escape will exit the full-screen mode
root.mainloop()
