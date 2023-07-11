import numpy as np
from scipy import signal

from ..BaseBlock import BaseBlock

class LowPassFilter(BaseBlock):
    def __init__(self, sample_rate, cutoff_frequency=100e3, transition_width=100e3, offset_frequency=0):
        BaseBlock.__init__(self)
        self.cutoff_frequency = cutoff_frequency
        self.transition_width = transition_width
        self.offset_frequency = offset_frequency
        self.sample_rate = sample_rate
        self.STOP = False

        self.calculateFilterParameters()


    def calculateFilterParameters(self):
        nyq_rate = self.sample_rate / 2.0
        t_width = self.transition_width / nyq_rate
        c_width = self.cutoff_frequency / nyq_rate
        attenuation = 60.0
        # Low pass filter
        N, beta = signal.kaiserord(attenuation, t_width)
        taps = signal.firwin(N, c_width, window=('kaiser', beta))
        self.taps = taps

    def run(self, samples):
        if self.offset_frequency != 0:
            w = -1.0j * 2.0 * np.pi * \
                (self.offset_frequency / self.sample_rate) * np.arange(len(samples))
            samples = samples * np.exp(w)
        
        # Low pass filter
        filtered = signal.lfilter(self.taps, 1.0, samples)
        return filtered

        
        
