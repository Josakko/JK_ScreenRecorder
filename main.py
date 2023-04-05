import tkinter as tk
from tkinter import filedialog
import threading
import time
import cv2
import numpy as np
import pyautogui
from PIL import Image, ImageTk, ImageGrab


class JK_ScreenRecorder(tk.Tk):
    def __init__(self):
        super().__init__()
        window_width = 1300
        window_hight = 800
        
        global monitor_hight, monitor_width
        monitor_width = self.winfo_screenwidth()
        monitor_hight = self.winfo_screenheight()
        
        x = (monitor_width / 2) - (window_width / 2)
        y = (monitor_hight / 2) - (window_hight / 2)

        self.geometry(f'{window_width}x{window_hight}+{int(x)}+{int(y)}')
        self.iconbitmap("JK.ico")
        self.title("JK ScreenRecorder")
        self.config(bg="#dbdbdb")
        self.protocol("WM_DELETE_WINDOW", self.quit)
        
        
        self.font = ("Arial", 14) #, font=self.font
        self.blank = tk.PhotoImage(file="blank.png")
        
        self.info_lbl = tk.Label(self, text="Preview", font=("Arial", 16), bg="#dbdbdb")
        self.info_lbl.pack(pady=20)
        
        self.preview_lbl = tk.Label(self, bg="#dbdbdb", image=self.blank)
        self.preview_lbl.pack()
        
        self.record_btn = tk.Button(self, text="Start Recording", command=self.toggle_recording, state="disabled", font=self.font, width=20)
        self.record_btn.pack(side=tk.LEFT, pady=10, padx=10)
        
        self.select_file_btn = tk.Button(self, text="Select Output File", command=self.select_file, font=self.font, width=20)
        self.select_file_btn.pack(pady=10, side=tk.LEFT, padx=10)
                
        self.quit_button = tk.Button(self, text="Quit", command=self.quit, font=self.font, width=20)
        self.quit_button.pack(pady=10, side=tk.RIGHT, padx=10)
        
        
        self.filename = None
        self.recording = False
        self.recording_thread = None
        
    def load_settings(self):
        
        pass
        
    def select_file(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Video File", "*.mp4")])
        if self.filename:
            self.record_btn.configure(state="normal")
    
    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.record_btn.configure(text="Stop Recording")
            self.recording_thread = threading.Thread(target=self.record)
            self.recording_thread.start()
        else:
            self.recording = False
            self.record_btn.configure(text="Start Recording", state="disabled")
            self.preview_lbl.configure(image=self.blank)
    
    def record(self):
        resolution = pyautogui.size()
        codec = cv2.VideoWriter_fourcc(*"mp4v")
        
        fps = 20.0
        delay = 0.0001
        #prev = 0
        
        out = cv2.VideoWriter(self.filename, codec, fps, resolution)
        
        while self.recording:
            #img = pyautogui.screenshot()
            img = ImageGrab.grab()
            
            #time_elapsed = time.time() - prev
            
            #if time_elapsed > 1.0 / fps:
            #   prev = time.time()
            frame = np.array(img)
            
            preview_img = cv2.resize(frame, (640, 360))
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
            
            #preview_img = cv2.cvtColor(preview_img, cv2.COLOR_BGR2RGB)
            preview_img = Image.fromarray(preview_img)
            preview_img = ImageTk.PhotoImage(image=preview_img)
            self.preview_lbl.configure(image=preview_img)
            self.preview_lbl.image = preview_img
            
            time.sleep(delay)
        out.release()

    def quit(self):
        if self.recording == True:
            self.quit_button.configure(state="disabled")
            self.recording = False
            self.record_btn.configure(text="Start Recording", state="disabled")
            self.preview_lbl.configure(image=self.blank)
            #exit()
            #self.destroy()
        else:
            self.quit_button.configure(state="disabled")
            self.record_btn.configure(text="Start Recording", state="disabled")
            #exit()
            self.destroy()
        
if __name__ == "__main__":
    app = JK_ScreenRecorder()
    app.mainloop()
