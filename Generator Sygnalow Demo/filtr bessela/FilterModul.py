from scipy import signal
import numpy as np


class Filters:
    def __init__(self, signal, ftype, cutoff, btype, order=3, fs=44100):
        self.ftype = ftype
        self.order = order
        self.cutoff = cutoff
        self.fs = fs
        self.btype = btype
        self.signal = signal

    def creating_filter(self):
        filter_types = {
            'Filtr Butterwortha': signal.butter,
            'Filtr Czebyszewa': signal.cheby1,
            'Filtr Bessela': signal.bessel
        }

        filter_kinds = {
            "Dolnoprzepustowy": 'low',
            "Górnoprzepustowy": 'high',
            "Środkowoprzepustowy": 'band',
            "Środkowozaporowy": 'bandstop'
        }

        for i in range(len(self.cutoff)):
            self.cutoff[i] = self.cutoff[i].replace("'", "")

        print (self.cutoff)

        # Ensure self.cutoff is a numeric type
        if isinstance(self.cutoff, list) and all(isinstance(c, (int, float)) or (isinstance(c, str) and c.strip()) for c in self.cutoff):
            for c in self.cutoff:
                print(c)
            cutoff_value = [int(c) / (0.5 * self.fs) for c in self.cutoff]

        else:
            if self.btype == "Dolnoprzepustowy":    
                print (self.cutoff[1])
            else:
                print (self.cutoff[0])
            
            cutoff_value = int(self.cutoff[0]) / (0.5 * self.fs) if self.btype == "Dolnoprzepustowy" else int(self.cutoff[1]) / (0.5 * self.fs)
        
            if self.ftype == "Filtr Czebyszewa":
                a, b = filter_types[self.ftype](N = int(self.order),rp = 0.5 , Wn = cutoff_value, btype = filter_kinds[self.btype])
            else:
                a, b = filter_types[self.ftype](N = int(self.order), Wn = cutoff_value, btype = filter_kinds[self.btype])
        print (f"wspolczyniki {a, b}")
        filtered_signal = signal.filtfilt(a, b, self.signal)

        return filtered_signal



