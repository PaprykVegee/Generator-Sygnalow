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
            "Œrodkowoprzepustowy": 'band',
            "Œrodkowozaporowy": 'bandstop'
        }

        a, b = filter_types[self.ftype](self.order, self.cutoff/(0.5*self.fs), filter_kinds[self.btype])

        filtered_signal = signal.filtfilt(a, b, self.signal)
        return filtered_signal


