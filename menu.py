import tkinter as tk
import os, sys
import threading, subprocess, keyboard
from tkinter import *
from PIL import Image, ImageTk
from toplevel import Newlv

altAccount = 0

class Menu():
    def __init__(self, window):
        self.window = window
        self.gagThumbnail = None  # Placeholder for image reference
        self.tk_image = None      # Placeholder for PhotoImage reference
        self.reruns = 0

    def onClose(self):
        keyboard.unhook_all()    
        self.window.destroy()
        for thread in threading.enumerate():
            if thread != threading.current_thread():
                thread.join(timeout=0.1)  # Try to close nicely first
    
        # Destroy the window

        subprocess.run(["taskkill", "/F", "/PID", str(os.getpid())], shell=True)
        os._exit(0)    

    def guiBuilder(self):
        # Window configuration
        root = self.window
        xGeo, yGeo = 600, 800

        root.geometry(f"{xGeo}x{yGeo}")
        root.title("Grow A Garden Multi Alt Macro")
        root.config(background="#292928")
        root.resizable(False, False)
        
        # Load image with Pillow for better handling
        # imagePath = self.resource_path("GAG Thumbnail.png")
        # img = Image.open(imagePath)
        img = Image.open("GAG Thumbnail.png")
        self.gagThumbnail = ImageTk.PhotoImage(img)
        root.iconphoto(True, self.gagThumbnail)
        self.photoResizer(img, xGeo, yGeo)

        # Entry 
        altNumEntry = Entry()
        altNumEntry.config(font=("Comic Sans MS", 10), bd=0, highlightthickness=0)
        addPlaceholder(altNumEntry, "Number of alts")
        altNumEntry.config(width=20)
        altNumEntry.pack(pady=(20,10), ipady=20)

        # Start 
        startBtn = Button(root, text = 'Start')
        startBtn.config(command=lambda: startBtnEvent(altNumEntry, root, self))
        startBtn.config(font=("Comic Sans MS", 25, 'bold'), width=15, height=1, bd=0, highlightthickness=0, fg="White")
        startBtn.config(bg="#181818", activebackground="#333333")
        startBtn.pack(pady=(10,0))

    # Convert to Tkinter PhotoImage and keep reference
    def photoResizer(self, picture, x, y):
            # Calculate scaling to fit window
        max_width = x - 200
        max_height = y - 200
        picture.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(picture)
        label = Label(self.window, image=self.tk_image, highlightthickness=0, bd=0)
        label.pack(pady=(60, 0))
        
# Creates a place holder text for our entry
def addPlaceholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='grey')
    
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, 'end')
            entry.config(fg='black')
    
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg='grey')
    
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)


# When you pass in the number of alt accounts you want to use
# TODO: Later we may find out whats the max number of alt accounts we could pass through and limit it
def startBtnEvent(altValue, root, menu):
    altNum = altValue.get().strip()
    # altNum = int(altNum)

    # TODO: Make it so if its none it sets to my default resolution
    if altNum.isdigit() and int(altNum)>0:   
        menu.reruns = int(altNum)
        root.withdraw()
        newWindow = Toplevel()
        toplv = Newlv(newWindow, menu.reruns)
        toplv.newlvBuilder()
        
    else:
        root.focus_force()
        altValue.delete(0, 'end')
        addPlaceholder(altValue, "Enter a valid number")
      
 
        

    



