import numpy as np

class SpectralAnalysis:

    def __init__(self, time, amplitude, dt):
        self.time = time
        self.amplitude = np.array(amplitude)
        self.dt = dt

        self.freq = np.fft.fftfreq(len(np.fft.fft(np.array(self.amplitude))), d=self.dt)
        self.indeksy_nieujemne = np.where(self.freq >= 0)
        self.freq_nieujemne = self.freq[self.indeksy_nieujemne]
    def DFT_transform(self):
        DFT_ = np.fft.fft(self.amplitude)
        len_DFT = len(DFT_)
        ampli = 2 * np.abs(DFT_) / len_DFT

        
        ampli_nieujemne = ampli[self.indeksy_nieujemne]

        return self.freq_nieujemne, ampli_nieujemne

    def energy_spectral_density(self):
        DFT_ = np.fft.fft(self.amplitude)
        DFT_ = DFT_[self.indeksy_nieujemne]
        ESD = 2 * (self.dt**2) * np.conj(DFT_) * DFT_

        return self.freq_nieujemne, ESD

    def power_spectral_density(self):
        ESD = self.energy_spectral_density()
        # Ucinamy self.time do długości ESD
        time_trimmed = self.time[:len(ESD)]
        PSD = ESD / time_trimmed

        return self.freq_nieujemne, PSD

    def power_spectrum(self):
        DFT_ = np.fft.fft(self.amplitude)
        DFT_ = DFT_[self.indeksy_nieujemne]
        PS = (2 * np.conj(DFT_) * DFT_) / len(DFT_)

        return self.freq_nieujemne, PS

    def Power_of_signal(self):
        power = sum([ampli**2 for ampli in self.amplitude]) / len(self.amplitude)

        return power

    def Energy_of_signal(self):
        energy = sum(ampli**2 for ampli in self.amplitude) * self.dt

        return energy
