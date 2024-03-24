import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sounddevice as sd
import numpy as np
import time

class SoundRecorder():
    def __init__(self, master,x, y, w, h, signal=None):
        self.master = master
        self.signal = signal
        self.recording = None  # Add initialization of recording

        # Creating frame and placing using place()
        self.frame = tk.Frame(self.master, bg="#FFFACD")
        self.frame.place(x=x, y=y, width=w, height=h)  # Adjust width, height, x, and y here

        # Title of the frame
        title_label = tk.Label(self.frame, text="Sound recorder", font=("TkDefaultFont", 12, "bold"), fg="red", bg="#FFFACD")
        title_label.place(x=30, y=30)

        # Label for delay and entry for delay
        label_delay = tk.Label(self.frame, text="Delay (s):", bg="#FFFACD")
        label_delay.place(x=30, y=70)

        self.entry_delay = tk.Entry(self.frame)
        self.entry_delay.place(x=120, y=70)

        # Label and entry for recording time
        label_recording = tk.Label(self.frame, text="Recording time (s):", bg="#FFFACD")
        label_recording.place(x=30, y=100)

        self.entry_recording = tk.Entry(self.frame)
        self.entry_recording.place(x=160, y=100)

        # Define button style
        style = ttk.Style()
        style.configure("Custom.TButton", background="#FFE57F")

        # Record button
        self.record_button = ttk.Button(self.frame, text="Record", style="Custom.TButton", command=self.record)
        self.record_button.place(x=50, y=130)

        # Playback button
        self.playback_button = ttk.Button(self.frame, text="Playback", style="Custom.TButton", command=self.play)
        self.playback_button.place(x=160, y=130)

        # Exit button
        self.exit_button = ttk.Button(self.frame, text="Exit",  style="Custom.TButton", command=self.exit_program)
        self.exit_button.place(x=105, y=170)

    # Method to exit the program
    def exit_program(self):
        self.frame.destroy

    # Record method
    def record(self):
        try:
            record_time = float(self.entry_recording.get())
            delay = float(self.entry_delay.get())

            if record_time <= 0 or delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Value must be positive number")
            return

        # Reset value when the method is called
        if self.recording is not None:
            self.recording = None

        self.record_button.config(state="disabled")
        self._record_thread(record_time, delay)

    # Recording thread
    def _record_thread(self, record_time, delay):
        sample_rate = 44100
        try:
            time.sleep(delay)
            recording = sd.rec(int(record_time * sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32)
            print(f"record_time: {int(record_time * sample_rate)}")
            time.sleep(record_time + delay)  # Wait for recording to finish and delay

            self.recording = recording[:, 0]
            self.playback_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during recording: {str(e)}")
        finally:
            self.record_button.config(state="normal")

    # Playback method
    def play(self):
        if self.signal is not None:
            signal = self.signal
        else:
            signal = self.recording

        if signal is not None:  # Check if there is a recording to play
            try:
                sd.play(signal)
                sd.wait()
            except Exception as e:
                messagebox.showerror("Error", f"{str(e)}")
        else:
            messagebox.showwarning("Warning", "No recording to play")




