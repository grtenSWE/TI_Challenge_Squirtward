from tkinter import *
from PIL import Image, ImageTk
import os


# functions
def get_image(frame, bg, filepath, resize):
    """returns a working image label"""
    IMG = Image.open(filepath)
    image = ImageTk.PhotoImage(IMG.resize(resize))
    img_lbl = Label(frame, image=image, bg=bg)
    img_lbl.image = image
    return img_lbl


# main GUI class
class GUI:
    """this class runs the interface"""
    def __init__(self, parent):
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

        self.screen = ""
        self.current_screen = ""
        self.current_stock_cards = []

        # Initialize the full-screen black background
        self.main = Frame(parent, bg='black')
        self.main.pack(fill=BOTH, expand=True)

       

        self.on = Frame(self.main, bg='gray')
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
        bg = get_image(self.main, 'white', 'face_pics/Annoy_Squidward.jpg', (850, 850))
        bg.pack(expand=True,anchor=S)

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
        pass


# mainloop
root = Tk()
GUI(root)
root.title("SquirtWard Face")
root.attributes("-fullscreen", True)  # Make the window full-screen
root.bind("<Escape>", lambda e: root.destroy())  # Pressing Escape will exit the full-screen mode
root.mainloop()
