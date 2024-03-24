from math import exp
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Canvas, messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Spectral_Analise import SpectralAnalysis
from Filtr_modul import Filters
from Sound_Record import SoundRecorder
import time

def sinusoidal_signal(amplitude, frequency, t, phase_shift=0):
    # t = np.linspace(0, 1, 44100, endpoint=False)
    return amplitude * np.sin(2 * np.pi * frequency * t + phase_shift)

def square_signal(amplitude, frequency, t, phase_shift=0):
    # t = np.linspace(0, 1, 44100, endpoint=False)
    return amplitude * np.sign(np.sin(2 * np.pi * frequency * t + phase_shift))

def triangle_signal(amplitude, frequency, t, phase_shift=0):
    # t = np.linspace(0, 1, 44100, endpoint=False)
    return amplitude * np.arcsin(np.sin(2 * np.pi * frequency * t + phase_shift))

class SignalGenerator():

    def __init__(self, master):
        self.master = master
        self.master.title("Signal Generator")

        # Geometry of master 
        self.master.geometry('800x500')
        self.master.configure(bg="#FFFACD")

        # Label X coordinat and Entry X coordinat
        X_label = 20
        X_Entry = 90

        Y_label = 30
        
        # Title
        Title_signal = tk.Label(self.master, text="Paramiter of signal", font=("TkDefaultFont", 12, "bold"), fg="red", bg="#FFFACD")
        Title_signal.place(x=X_label+30, y=Y_label-25)

        # Amplitude label and entry
        Amplitude_label = tk.Label(self.master, text="Amplitude:",  bg="#FFFACD")
        Amplitude_label.place(x=X_label, y=Y_label)

        self.Amplitude_entry = tk.Entry(self.master)
        self.Amplitude_entry.place(x=X_Entry, y=Y_label)

        # Frequency label and entry
        frequency_label = tk.Label(self.master, text="Frequency:",  bg="#FFFACD")
        frequency_label.place(x=X_label, y=Y_label*2)

        self.frequency_entry = tk.Entry(self.master)
        self.frequency_entry.place(x=X_Entry, y=Y_label*2)

        # Optimenu for unit of frequency
        self.frequency_unit_var = tk.StringVar(self.master)
        self.frequency_unit_var.set("Hz")
        frequency_unit_menu = ttk.OptionMenu(self.master, self.frequency_unit_var, "", "Radian", "Hz")
        frequency_unit_menu.place(x=X_label+200, y=Y_label*2-5)

        # Phase shift label and entry
        Phase_shift_label = tk.Label(self.master, text="Phase shift:",  bg="#FFFACD")
        Phase_shift_label.place(x=X_label, y=Y_label*3)

        self.Phase_shift_entry = tk.Entry(self.master)
        self.Phase_shift_entry.place(x=X_Entry, y=Y_label*3)

        # Type of signal label and optimenu
        type_of_signal_label = tk.Label(self.master, text="Type of signal:",  bg="#FFFACD")
        type_of_signal_label.place(x=X_label, y=Y_label*4)

        list_of_typeSignal = ["", "sinusoidal", "rectangular", "triangular"]
        self.type_of_signal_var = tk.StringVar(self.master)
        self.type_of_signal_var.set('sinusoidal')
        type_of_siganl_opti_menu = ttk.OptionMenu(self.master, self.type_of_signal_var, *list_of_typeSignal)
        type_of_siganl_opti_menu.place(x=X_Entry+20, y=Y_label*4-5)

        # Generate signal button
        generate_button = ttk.Button(self.master, text="Generate Signal",  style="Custom.TButton", command=self.generate_signal)
        generate_button.place(x=X_label+60, y=Y_label*5)

        # Paramiter of canvas
        # Title
        Title_canvas_opti = tk.Label(self.master, text="Paramiter of Canvas", font=("TkDefaultFont", 12, "bold"),  fg="red", bg="#FFFACD")
        Title_canvas_opti.place(x=X_label+30, y=Y_label*7)

        # Type of plot
        Type_plot_label = tk.Label(self.master, text="Type of graph:", bg='#FFFACD')
        Type_plot_label.place(x=X_label, y=Y_label*8)

        self.Type_plot_var = tk.StringVar(self.master)
        Plot_type = ["", "Generated signal", "DFT", "ESD", "PS", "Signal after filtering"]
        self.Type_plot_var.set("Generated signal")
        self.Type_plot_var.trace('w', self.update_graph)
        Type_plot_optimenu = ttk.OptionMenu(self.master, self.Type_plot_var, *Plot_type)
        Type_plot_optimenu.place(x=X_Entry+20, y=Y_label*8-5)

        # Type of signal
        Type_filtre_label = tk.Label(self.master, text="Type of filter:", bg='#FFFACD')
        Type_filtre_label.place(x=X_label, y=Y_label*9)

        self.Type_filtre_var = tk.StringVar(self.master)
        Filtr_type = ["", "No filter", "Chebyshev filter", "Bessel filter", "Butterworth filter"]
        self.Type_filtre_var.set("No filter")
        self.Type_filtre_var.trace('w', self.update_filtre)
        Filtre_type_optmenu = ttk.OptionMenu(self.master, self.Type_filtre_var, *Filtr_type)
        Filtre_type_optmenu.place(x=X_Entry+20, y=Y_label*9-5)
        

        style = ttk.Style()
        style.theme_use('alt')  #'clam', 'default', 'alt', etc.
        # Config for Optimenu
        style.configure('TMenubutton', background='#FFE57F')


        # Canvas look
        self.fig, (self.ax, self.ax_components) = plt.subplots(nrows=2, gridspec_kw={'height_ratios': [3, 1]})

        # Set background color of the figure
        self.fig.patch.set_facecolor('#FFFACD')
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().place(x=X_Entry+230, y=Y_label)


        # Clean button
        clear_button = ttk.Button(self.master, text="clear signal", style="Custom.TButton",  command=self.clear_canvas)
        clear_button.place(x=X_Entry+20, y=Y_label*12-5)

        # Voice recorder Button
        voice_recorder_button = ttk.Button(self.master, text="Voice record", style="Custom.TButton", command=self.initialize_recorder)
        voice_recorder_button.place(x=1000, y=250)


        # Config for button
        style.configure("Custom.TButton", background="#FFE57F")


        # Checkbox to create new canvas to look filtered signal and normal signal
        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(self.master, text="Plot filtered and unfiltered signal", variable=self.checkbox_var, bg="#FFFACD", command=self.checkbox_click)

        self.signals = []
        self.signal_name = {}

        # Crop on X axis (Label, Entry, Button)
        crop_label = tk.Label(self.master, text="Zoom X axis:", bg="#FFFACD")
        crop_label.place(x=500, y=30)

        self.crop_entry = tk.Entry(self.master)
        self.crop_entry.place(x=590, y=30)

        crop_button = ttk.Button(self.master, text="zoom", style="Custom.TButton", command=self.zoom_X_axis)
        crop_button.place(x=545, y=60)


        """
        # time varable
        if hasattr(self, 'freq_list'):
            t = np.linspace(0, 1 / max(self.freq_list), 44100, endpoint=False)
            self.ax.plot(t, self.sum_signals)
        else:
            t = np.linspace(0, float(self.app.entry_recording.get())/44100, 44100, endpoint=False)
        """

        # Optimenu and label for signal to remove
        signal_label = tk.Label(self.master, text="Signal list", bg="#FFFACD")
        signal_label.place(x=1000, y=150)

        self.signal_optimenu_var = tk.StringVar()
        ############# maybe trace fun
        self.signal_optimenu = ttk.OptionMenu(self.master, self.signal_optimenu_var, *self.signal_name)
        self.signal_optimenu.place(x=1000, y=180)

        remove_siganl_button = ttk.Button(self.master, style="Custom.TButton", text="remove signal", command=self.remove_signal)
        remove_siganl_button.place(x=1000, y=210)

        # refresh button if is any problem with display graph
        refresh_button = ttk.Button(self.master, style="Custom.TButton", text="Refrece graph", command=self.refrece)
        refresh_button.place(x=590, y=500)
    
    def plot_dft(self):
        freq, ampli = self.spectral_analisys_instance.DFT_transform()
        self.ax.clear()
        self.ax.plot(freq, ampli)
        self.canvas.draw()

    def plot_esd(self):
        freq, esd = self.spectral_analisys_instance.energy_spectral_density()
        self.ax.clear()
        self.ax.plot(freq, esd)
        self.canvas.draw()

    def plot_ps(self):
        freq, ps = self.spectral_analisys_instance.power_spectrum()
        self.ax.clear()
        self.ax.plot(freq, ps)
        self.canvas.draw()

    def update_graph(self, *args):
        self.t = np.linspace(0, 1, 44100, endpoint=False)
        if hasattr (self, 'app'):
            self.t = np.linspace(0, int(self.app.entry_recording.get()), len(self.sum_signals), endpoint=False)

        try:
            self.spectral_analisys()  # Ensure spectral_analisys_instance is initialized
            plot_type = self.Type_plot_var.get()
            if plot_type == "DFT":
                self.plot_dft()
                if hasattr(self, 'checkbox'):
                    self.checkbox.place_forget()
            elif plot_type == "ESD":
                self.plot_esd()
                if hasattr(self, 'checkbox'):
                    self.checkbox.place_forget()
            elif plot_type == "PS":
                self.plot_ps()
                if hasattr(self, 'checkbox'):
                    self.checkbox.place_forget()
            elif plot_type == "Generated signal":
                self.plot_generated_signal()
                if hasattr(self, 'checkbox'):
                    self.checkbox.place_forget()
            elif plot_type == "Signal after filtering":
                self.plot_signal_after_filtering()
        except AttributeError as e:
            print(e)
            self.Type_plot_var.set("Generated signal")
            messagebox.showerror("Error", "No signal to calculate spectral analisys") 

    def spectral_analisys(self):
        self.spectral_analisys_instance = SpectralAnalysis(time=self.t, amplitude=self.sum_signals, dt=1/44100)


    def plot_generated_signal(self):
        print("debug")
        self.ax.clear()
        #self.spectral_analisys()
        self.ax.plot(self.t, self.sum_signals)
        self.canvas.draw()

    def plot_signal_after_filtering(self):
        self.ax.clear()

        self.ax.plot(self.t, self.filtered_signal)
        self.canvas.draw()

        if not hasattr(self, 'checkbox'):
            self.checkbox_var = tk.BooleanVar()
            self.checkbox = tk.Checkbutton(self.master, text="Plot filtered and unfiltered signal", variable=self.checkbox_var, bg="#FFFACD", command=self.checkbox_click)
            self.checkbox.place(x=1000, y=100)
        else:
            self.checkbox.place(x=1000, y=100)

    ################################################## Fun for plot_signal_after_filtering ######################################
    def checkbox_click(self):
        #if hasattr(self, 'freq_list'):
            #t = np.linspace(0, 1/max(self.freq_list), 44100, endpoint=False)
        #else:
            #t = np.linspace(0, float(self.app.entry_recording.get()), 44100, endpoint=False)
        if self.checkbox_var.get():
            fig, (self.ax_left, self.ax_right) = plt.subplots(nrows=1, ncols=2)
            self.ax_left.plot(self.t, self.sum_signals)
            self.ax_left.set_title("Before filtre")
            self.ax_right.plot(self.t,self.filtered_signal)
            self.ax_right.set_title("After filtred")
            fig.patch.set_facecolor('#FFFACD')
            self.canvas2 = FigureCanvasTkAgg(fig, master=self.master)
            self.canvas2.get_tk_widget().place(x=330, y=30)
            self.canvas2.draw()
            print("True")
        else:
            if hasattr(self, 'canvas2'):
                self.canvas2.get_tk_widget().destroy()
                del self.canvas2
            
    ###########################################################################################################################

    ######################################################## Filter ###########################################################
    def applay_filter(self):
        try:
            filtre_type = self.Type_filtre_var.get()
            filtre_subtype = self.filtre_subtyp_var.get()

            print(self.lowpass_entry.get())
            print(self.high_pass_entry.get())

            if self.lowpass_entry.get() is not None:
                lower = self.lowpass_entry.get()

            if self.high_pass_entry.get() is not None:
                upper = self.high_pass_entry.get()

            print ([lower, upper])
            type_of_filtr = self.Type_filtre_var.get()
            filters = Filters(signal=self.sum_signals,
                              ftype=filtre_type, 
                              cutoff=[lower, upper], 
                              btype=filtre_subtype,
                              order=int(self.order_entry.get()),
                              fs=44100)
            self.filtered_signal = filters.creating_filter()

            
        except AttributeError as e:
            messagebox.showerror("Error", f"{e}")

        except ValueError as e:
           messagebox.showerror("Error", f" {e} Lower limit and Higher limit must be a digit or order of filtre must be intiger")
           print(e)

    def update_filtre(self, *args):
        if not self.Type_filtre_var.get() == "No filter":
            # If label not exist create
            if not hasattr(self, 'filtre_type_label'):
                self.filtre_type_label = tk.Label(self.master, text="", font=("TkDefaultFont", 12, "bold"), bg="#FFFACD")
                self.filtre_type_label.place(x=20, y=600)

                # Label for Optimenu
                self.Optimenu_label = tk.Label(self.master, text="type of filter:", bg="#FFFACD")
                self.Optimenu_label.place(x=20, y=630)

                # Optimenu for subtype
                self.filtre_subtyp_var = tk.StringVar(self.master)
                filtr_subtype_list = ["", "Lowpass", "High Pass", "Bandpass", "Bandstop"]
                self.filtre_subtyp_var.set("Lowpass")
                self.filtre_subtype_optimenu = ttk.OptionMenu(self.master, self.filtre_subtyp_var, *filtr_subtype_list)
                self.filtre_subtype_optimenu.place(x=100, y=625)

                # Function to update labels and entries
                def update_labels_and_entries(*args):
                    if self.filtre_subtyp_var.get() == "Lowpass":
                        self.order_label.place_forget()
                        self.order_entry.place_forget()

                        self.lowpass_label.place(x=20, y=660)
                        self.lowpass_entry.place(x=100, y=660)

                        self.order_label.place(x=20, y=690)
                        self.order_entry.place(x=100, y=690)

                        self.high_pass_label.place_forget()
                        self.high_pass_entry.place_forget()
                        self.high_pass_entry.insert(0, "")

                    elif self.filtre_subtyp_var.get() == "High Pass":
                        self.lowpass_label.place_forget()
                        self.lowpass_entry.place_forget()
                        self.lowpass_entry.insert(0, "")
                        self.order_label.place_forget()
                        self.order_entry.place_forget()

                        self.high_pass_label.place(x=20, y=660)
                        self.high_pass_entry.place(x=100, y=660)

                        self.order_label.place(x=20, y=690)
                        self.order_entry.place(x=100, y=690)

                    elif self.filtre_subtyp_var.get() in ["Bandpass", "Bandstop"]:
                        self.lowpass_label.place(x=20, y=660)
                        self.lowpass_entry.place(x=100, y=660)

                        self.high_pass_label.place(x=20, y=690)
                        self.high_pass_entry.place(x=100, y=690)

                        self.order_label.place_forget()
                        self.order_entry.place_forget()

                        self.order_label.place(x=20, y=720)
                        self.order_entry.place(x=100, y=720)

                # Labels and entries
                self.lowpass_label = tk.Label(self.master, text="Lower limit:", bg="#FFFACD")
                self.lowpass_entry = tk.Entry(self.master)

                self.high_pass_label = tk.Label(self.master, text="High limit:", bg="#FFFACD")
                self.high_pass_entry = tk.Entry(self.master)

                self.order_label = tk.Label(self.master, text="Order of Filter", bg="#FFFACD")
                self.order_entry = tk.Entry(self.master)

                # Button to accept val of filter
                self.Accep_Button = tk.Button(self.master, text="Applay Filtre", bg="#FFE57F", command=self.applay_filter)
                self.Accep_Button.place(x=30, y=750)

                # Command to update labels and entries when subtype changes
                self.filtre_subtyp_var.trace("w", update_labels_and_entries)

            else:
                self.filtre_subtyp_var.set("Lowpass")
                # If label exists, just update subtype var
                # This will trigger the update of labels and entries
                # through the trace we set earlier

            # Update
            self.filtre_type_label.config(text=f"Filtr type: {self.Type_filtre_var.get()}")

        else:
            # If no filter selected, destroy labels and entries
            if hasattr(self, 'filtre_type_label'):
                self.filtre_type_label.destroy()
                del self.filtre_type_label

            if hasattr(self, 'Optimenu_label'):
                self.Optimenu_label.destroy()
                del self.Optimenu_label

            if hasattr(self, 'filtre_subtype_optimenu'):
                self.filtre_subtype_optimenu.destroy()
                del self.filtre_subtype_optimenu

            if hasattr(self, 'lowpass_label'):
                self.lowpass_label.destroy()
                del self.lowpass_label

            if hasattr(self, 'lowpass_entry'):
                self.lowpass_entry.destroy()
                del self.lowpass_entry

            if hasattr(self, 'high_pass_label'):
                self.high_pass_label.destroy()
                del self.high_pass_label

            if hasattr(self, 'high_pass_entry'):
                self.high_pass_entry.destroy()
                del self.high_pass_entry
            
            if hasattr(self, 'order_label'):
                self.order_label.destroy()
                del self.order_label

            if hasattr(self, 'order_entry'):
                self.order_entry.destroy()
                del self.order_entry

            # Weird becouse on button obiect I dont needed if has... structure
            self.Accep_Button.destroy()

    #######################################################################################################################################
    
    
    def clear_canvas(self):
        # Clean data
        self.signals = []
        self.signal_name = {}

        # Clean axs
        self.ax.clear()
        self.ax_components.clear()

        try:
            self.ax_left.clear()
            self.ax_right.clear()
        except AttributeError:
            pass

        # Clen remove manu
        menu = self.signal_optimenu['menu']
        menu.delete(0, 'end')

        self.canvas.draw()
        self.t = np.linspace(0, 1, 44200, endpoint=False)

    def generate_signal(self):
        self.t = np.linspace(0, 1, 44100, endpoint=False)

        if hasattr (self, 'app'):
            self.t = np.linspace(0, int(self.app.entry_recording.get()), len(self.sum_signals), endpoint=False)

        try:
            amplitude = float(self.Amplitude_entry.get())

            # Check if frequency unit is Hz or Radian
            if self.frequency_unit_var.get() == "Hz":
                frequency = float(self.frequency_entry.get())
            else:
                # Convert frequency from radian to Hz
                frequency = float(self.frequency_entry.get()) / (2 * np.pi)

            phase_shift = float(self.Phase_shift_entry.get())

            if self.type_of_signal_var.get() == "sinusoidal":
                signal = sinusoidal_signal(amplitude, frequency, self.t, phase_shift)
                signal_name = f"{amplitude}*sin(2*pi*{frequency} + {phase_shift})"

            elif self.type_of_signal_var.get() == "rectangular":
                signal = square_signal(amplitude, frequency, self.t, phase_shift)
                signal_name = f"{amplitude}*rect(2*pi*{frequency} + {phase_shift})"
            elif self.type_of_signal_var.get() == "triangular":
                signal = triangle_signal(amplitude, frequency, self.t, phase_shift)
                signal_name = f"{amplitude}*tri(2*pi*{frequency} + {phase_shift})"

            # Clear old canvas
            self.ax.clear()

            # signal name list
            self.signal_name[signal_name] = signal

            # Update the OptionMenu for signal list
            menu = self.signal_optimenu['menu']
            menu.delete(0, 'end')
            for signal_n in self.signal_name.keys():
                menu.add_command(label=signal_n, command=tk._setit(self.signal_optimenu_var, signal_n))

            self.signals.append(signal)
            self.sum_signals = np.sum(self.signals, axis=0)

            self.plot_generated_signal()
            # Component of signal
            # t = np.linspace(0, 1/ max(self.freq_list), 44100, endpoint=False)
            for signal in self.signals:
                self.ax_components.plot(self.t, signal)
            self.canvas.draw()

        except ValueError:
            messagebox.showerror("Error", "Some of the input fields do not contain valid numbers")

    def remove_signal(self):
        signal_name = self.signal_optimenu_var.get()
        if signal_name in self.signal_name:
            del self.signal_name[signal_name]  # Usuwanie sygnału z listy nazw sygnałów
            self.signals = [signal for key, signal in self.signal_name.items()]  # Aktualizacja listy sygnałów bez usuwanego sygnału
            self.sum_signals = np.sum(self.signals, axis=0)  # Zaktualizowanie sumy sygnałów

            # Usunięcie opcji z OptionMenu
            menu = self.signal_optimenu['menu']
            menu.delete(0, 'end')
            for signal_n in self.signal_name.keys():
                menu.add_command(label=signal_n, command=tk._setit(self.signal_optimenu_var, signal_n))

            # Aktualizacja wykresu
            self.generate_signal()
            self.update_graph()
            self.canvas.draw()
        else:
            messagebox.showerror("Error", "Selected signal does not exist")

    def initialize_recorder(self):
        if hasattr(self, 'filtered_signal'):
            self.app = SoundRecorder(self.master, x=10, y=10, w=350, h=200, signal=self.filtered_signal)
        else:

            self.app = SoundRecorder(self.master, x=10, y=10, w=350, h=200)

        self.recording = self.app.recording

    def refrece(self):
        if hasattr(self, 'app'):
            self.sum_signals = self.app.recording
            self.update_graph()
            self.canvas.draw() 
        else:
            self.update_graph()
            self.canvas.draw() 

    # Zoom method
    def zoom_X_axis(self):
        print("Zooming X axis...") 
        try:
            x = float(self.crop_entry.get())  
            self.ax.set_xlim(0, x)  
            self.ax_components.set_xlim(0, x)
            print("Limits set successfully for main plot")  
            self.canvas.draw()  
            print("Canvas updated successfully")  
        except ValueError as e:
            messagebox.showerror("Error", "Zoom value must be a number")
        try:
            self.ax_left.set_xlim(0, x)
            self.ax_right.set_xlim(0, x)
        except AttributeError as e:
            print(f"ValueError: {e}")  



if __name__ == "__main__":
    root = tk.Tk()
    app = SignalGenerator(root)
    root.mainloop()