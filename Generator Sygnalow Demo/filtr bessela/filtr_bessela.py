import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import DFT
import FilterModul


def sinusoidal_signal(t, amplituda, czestotliwosc, przesuniecie_fazowe=0):
    if t is None:
        t = 0
    return amplituda * np.sin(2 * np.pi * czestotliwosc * t + przesuniecie_fazowe)

def square_signal(t, amplituda, czestotliwosc, przesuniecie_fazowe=0):
    if t is None:
        t = 0
    return amplituda * np.sign(np.sin(2 * np.pi * czestotliwosc * t + przesuniecie_fazowe))

def triangle_signal(t, amplituda, czestotliwosc, przesuniecie_fazowe=0):
    if t is None:
        t = 0
    return amplituda * np.arcsin(np.sin(2 * np.pi * czestotliwosc * t + przesuniecie_fazowe))

class SignalGeneratorApp:
    def __init__(self, master):
        # Inicjalizacja interfejsu użytkownika
        self.master = master
        self.master.title("Generator Sygnałów")

        # Etykiety i pola do wprowadzania danych
        self.amplitude_label = tk.Label(master, text="Amplituda:")
        self.amplitude_label.grid(row=0, column=0, sticky='w')

        self.amplitude_entry = tk.Entry(master)
        self.amplitude_entry.grid(row=0, column=1, sticky='w')

        self.frequency_label = tk.Label(master, text="Częstotliwość:")
        self.frequency_label.grid(row=1, column=0, sticky='w')

        self.frequency_entry = tk.Entry(master)
        self.frequency_entry.grid(row=1, column=1, sticky='w')

        self.phase_shift_label = tk.Label(master, text="Przesunięcie fazowe:")
        self.phase_shift_label.grid(row=2, column=0, sticky='w')

        self.phase_shift_entry = tk.Entry(master)
        self.phase_shift_entry.grid(row=2, column=1, sticky='w')

        # Optimenu dla sygnalu
        self.signal_type_label = tk.Label(master, text="Typ sygnału:")
        self.signal_type_label.grid(row=3, column=0, sticky='w')
        
        self.signal_type_var = tk.StringVar(master)
        self.signal_type_var.set("sinusoidalny")  # Początkowy wybór (Ustawienie domyslej wartosci OptionManu na sinusa)

        self.signal_type_menu = tk.OptionMenu(master, self.signal_type_var, "sinusoidalny", "prostokątny", "trójkątny")
        self.signal_type_menu.grid(row=3, column=1, sticky='w')

        # Optimenu dla rodzaju wykresu
        self.plot_type_label = tk.Label(master, text="Typ wykresu:")
        self.plot_type_label.grid(row=4, column=0, sticky='w')

        self.plot_type_var = tk.StringVar(master)
        self.plot_type_var.set("Sygnał generowany")  # Początkowy wybór (Ustawienie domyslej wartosci OptionManu na sygnał generowany)

        self.plot_type_menu = tk.OptionMenu(master, self.plot_type_var, "Sygnał generowany", "DFT", "ESD", "PSD", "Sygnał po filtracji")
        self.plot_type_menu.grid(row=4, column=1, sticky='w')

        # Optimenu dla rodzaja filtra 
        self.filter_type_label = tk.Label(master, text="Rodzaj Filtra")
        self.filter_type_label.grid(row=5, column=0, sticky='w')

        self.filter_type_var = tk.StringVar(master)
        self.filter_type_var.set("Brak filtra")

        self.filter_type_label = tk.OptionMenu(master, self.filter_type_var, "Brak filtra", "Filtr Czebyszewa", "Filtr Bessela", "Filtr Butterwortha")
        self.filter_type_label.grid(row=5, column=1, sticky='w')


        # Przyciski do generowania, wyświetlania i czyszczenia sygnałów
        self.generate_button = tk.Button(master, text="Generuj Sygnał", command=self.generate_signal)
        self.generate_button.grid(row=6, column=0, columnspan=2, pady=5, sticky='w')

        self.plot_button = tk.Button(master, text="Wykres", command=self.plot_signals)
        self.plot_button.grid(row=7, column=0, columnspan=2, pady=5, sticky='w')

        self.clear_button = tk.Button(master, text="Wyczyść listę", command=self.clear_signals)
        self.clear_button.grid(row=8, column=0, columnspan=2, pady=5, sticky='w')

        self.czas_obserwacji_label = tk.Label(master, text="Czas obserwacji (s):")
        self.czas_obserwacji_label.grid(row=9, column=0, sticky='w')

        self.czas_obserwacji_entry = tk.Entry(master)
        self.czas_obserwacji_entry.grid(row=9, column=1, sticky='w')

        # Wykresy i etykieta z równaniem aktualnego sygnału
        self.fig, (self.ax, self.ax_components) = plt.subplots(nrows=2, gridspec_kw={'height_ratios': [3, 1]})
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().grid(row=10, column=3, rowspan=10, padx=10, sticky='nsew')

        # Lista sygnałów i etykieta z równaniem
        self.signals = []
        self.equation_label = tk.Label(master, text="")
        self.equation_label.grid(row=11, column=0, columnspan=2, pady=5, sticky='w')
 
        # Zastosowanie dostosowywania rozmiarów wykresów do wielkości okna
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.fig.set_size_inches(6, 6, forward=True)  # Początkowy rozmiar wykresu
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=8, padx=10, sticky='nsew')
        self.t = None
    
    def create_filter_window(self):

        self.filter_type = self.filter_type_var.get()
        if self.filter_type != "Brak filtra":
            filter_window = tk.Toplevel(self.master)
            filter_window.title("Konfiguracja Filtra")

            filter_type_label = tk.Label(filter_window, text=f"Rodzaj Filtra: {self.filter_type}")
            filter_type_label.pack(pady=10)

            # Optimenu dla rodzaju filtra
            filter_subtype_label = tk.Label(filter_window, text="Rodzaj Filtra:")
            filter_subtype_label.pack(pady=5)

            filter_subtype_var = tk.StringVar(filter_window)
            filter_subtype_var.set("Dolnoprzepustowy")

            filter_subtype_menu = tk.OptionMenu(filter_window, filter_subtype_var, "Dolnoprzepustowy", "Górnoprzepustowy", "Środkowoprzepustowy", "Środkowozaporowy")
            filter_subtype_menu.pack(pady=5)

            # Funkcja, która obsługuje zmiany w rodzaju filtra
            # ten args jest tu po to zeby argumentu pozycyjne sie zmianialy (powjawialy i znikaly sie odchylki ze wzgeldu na wybor filtra)
            def on_filter_subtype_change(*args):
                self.type_of_filtr = filter_subtype_var.get()

                # Usuń istniejące pola
                for widget in filter_window.winfo_children():
                    if isinstance(widget, tk.Entry):
                        widget.destroy()
                    if isinstance(widget, tk.Label) and widget.cget("text") != f"Rodzaj Filtra: {self.filter_type}":
                        widget.destroy()
                    if isinstance(widget, tk.Button):
                        widget.destroy()
            
                # Warunki, które pokazują "lower limit" i "upper limit" ze względu na wybrany rodzaj filtra
                if self.type_of_filtr == "Dolnoprzepustowy":
                    lower_limit_label = tk.Label(filter_window, text="Lower Limit:")
                    lower_limit_label.pack(pady=5)

                    lower_limit_entry = tk.Entry(filter_window)
                    lower_limit_entry.pack(pady=5)

                    # diwny myk zeby mi sie wygenerowala zmianan ale zeby byla ona non i user nie mogl jej uzyc
                    upper_limit_entry = tk.Entry(filter_window)

                elif self.type_of_filtr == "Górnoprzepustowy":
                    upper_limit_label = tk.Label(filter_window, text="Upper Limit:")
                    upper_limit_label.pack(pady=5)

                    upper_limit_entry = tk.Entry(filter_window)
                    upper_limit_entry.pack(pady=5)

                    lower_limit_entry = tk.Entry(filter_window)

                else:
                    lower_limit_label = tk.Label(filter_window, text="Lower Limit:")
                    lower_limit_label.pack(pady=5)

                    lower_limit_entry = tk.Entry(filter_window)
                    lower_limit_entry.pack(pady=5)

                    upper_limit_label = tk.Label(filter_window, text="Upper Limit:")
                    upper_limit_label.pack(pady=5)

                    upper_limit_entry = tk.Entry(filter_window)
                    upper_limit_entry.pack(pady=5)

                # Stopień filtra 
                order_of_filtr_label = tk.Label(filter_window, text="Stopien filtra:")
                order_of_filtr_label.pack(pady = 5)

                order_of_filtr_entry = tk.Entry(filter_window)
                order_of_filtr_entry.pack(pady = 5)

                def get_value(order_of_filtr_entry, upper_limit_entry, lower_limit_entry):
                    if order_of_filtr_entry.get() is not None:
                        self.order = order_of_filtr_entry.get()
                    if upper_limit_entry.get() is not None:
                        self.upper = upper_limit_entry.get()
                    if lower_limit_entry.get() is not None:
                        self.lower = lower_limit_entry.get()

                    print ([self.filter_type, self.type_of_filtr, self.order,  [self.upper, self.lower]])

                    return [self.filter_type, self.type_of_filtr, self.order,  [self.lower, self.upper]]


                apply_button = tk.Button(filter_window, text="Zastosuj Filtr", command=lambda: get_value(order_of_filtr_entry, upper_limit_entry, lower_limit_entry)
                                                                                               or filter_window.destroy())
                apply_button.pack(pady=10)

            # Zarejestruj funkcję do wywołania po zmianie rodzaju filtra
            filter_subtype_var.trace_add('write', on_filter_subtype_change)

            # Wywołaj funkcję ręcznie, aby dostosować pola do początkowego rodzaju filtra
            on_filter_subtype_change()


    def generate_signal(self):
        # Generowanie sygnału na podstawie wprowadzonych danych
        try:
            amplitude = float(self.amplitude_entry.get())
            frequency = float(self.frequency_entry.get())
            # lista do limitowania wykresu DFT
            self.list_of_freq = []
            self.list_of_freq.append(frequency)
            phase_shift = float(self.phase_shift_entry.get())
            signal_type = self.signal_type_var.get()

            self.t = np.linspace(0, float(self.czas_obserwacji_entry.get()), 88200, endpoint=False)

            # Wybór funkcji sygnałowej
            if signal_type == "sinusoidalny":
                signal = sinusoidal_signal(self.t, amplitude, frequency, phase_shift)
                equation = f"{amplitude}*sin(2*pi*{frequency}*t + {phase_shift})"
            elif signal_type == "prostokątny":
                signal = square_signal(self.t, amplitude, frequency, phase_shift)
                equation = f"{amplitude}*sign(sin(2*pi*{frequency}*t + {phase_shift}))"
            elif signal_type == "trójkątny":
                signal = triangle_signal(self.t, amplitude, frequency, phase_shift)
                equation = f"{amplitude}*arcsin(sin(2*pi*{frequency}*t + {phase_shift}))"

            self.signals.append(signal)
            self.equation_label.config(text=equation)
        except ValueError:
            error_window = tk.Toplevel(root)
            error_text = "ERROR warosci muszą byc liczbami"
            label = tk.Label(error_window, text=error_text)
            label.pack(padx=20, pady=20)

    def DFT_signal(self):
            amplitude = float(self.amplitude_entry.get())
            frequency = float(self.frequency_entry.get())
            T = np.arange(0, len(self.t) / 44100, 1/44100)
            signal = DFT.SpectralAnalysis(time=T, amplitude=self.sum_signal, dt=1/44100)
            self.freq, self.ampli = signal.DFT_transform()
            self.ESD = signal.energy_spectral_density()
            self.PSD = signal.power_spectral_density()
    
    def applay_filter(self):
        try:
            filters = FilterModul.Filters(self.sum_signal, self.filter_type, 
                                           [self.lower, self.upper], 
                                           self.type_of_filtr, self.order)
            filtered_signal = filters.creating_filter()
            return filtered_signal
        except AttributeError:
            error_window = tk.Toplevel(root)
            error_text = "ERROR ustawienia filtra sa puste"
            label = tk.Label(error_window, text=error_text)
            label.pack(padx=20, pady=20)
            
            return self.sum_signal

    def plot_signals(self):
        # Wyświetlanie wykresów na podstawie wygenerowanych sygnałów
        if not self.signals or any(s is None for s in self.signals):
            return

        # sumowanie kolum dwu wymiarowej tablicy numpy
        self.sum_signal = np.sum(self.signals, axis=0)

        # rysowanie wykresu interferencji
        self.ax.clear()
        self.DFT_signal()
        if self.plot_type_var.get() == "Sygnał generowany":
            self.ax.plot(self.t, self.sum_signal)
            self.ax.set_title("Suma sygnałów")
            # rysowanie skladowych sygnalu
            for signal in self.signals:
                self.ax_components.plot(self.t, signal, alpha=0.5)
        
        elif self.plot_type_var.get() == "Sygnał po filtracji":
            self.ax.plot(self.t, self.applay_filter())

        elif self.plot_type_var.get() == "DFT":
            self.ax.plot(self.freq, self.ampli)
            self.ax.set_title("DFT - Widmo amplitudowe")
            self.ax_components.legend()

        elif self.plot_type_var.get() == "ESD":
            # Ustaw ograniczenia dla osi x
            self.ax.autoscale()

            self.ax.plot(self.freq, self.ESD)
            self.ax.set_title("ESD")
            self.ax_components.legend()

        elif self.plot_type_var.get() == "PSD":
            self.ax.plot(self.freq, self.PSD)
            self.ax.set_title("PSD")
            self.ax_components.legend()

            # Ustaw ograniczenia dla osi x
            #self.ax.set_xlim(0, max(self.list_of_freq) + 100)

        # Dostosowywanie rozmiarów wykresów
        self.fig.tight_layout()

        self.canvas.draw()

    def clear_signals(self):
        # Czyszczenie listy sygnałów i etykiety z równaniem
        self.signals = []

        # Usuwanie wykresow z glownego wykresu
        self.ax.clear()
        # Usuwanie wykresow z wykresu dolnego 
        self.ax_components.clear()
        self.equation_label.config(text="")

        # Przerysowanie pustych wykresów
        self.ax.figure.canvas.draw()

if __name__ == "__main__":
    # Uruchomienie aplikacji
    root = tk.Tk()
    app = SignalGeneratorApp(root)
    
    # Dodaj guzik "Konfiguruj Filtr"
    configure_filter_button = tk.Button(root, text="Konfiguruj Filtr", command=app.create_filter_window)
    configure_filter_button.grid(row=6, column=1, pady=5, sticky='w')

    root.mainloop()
