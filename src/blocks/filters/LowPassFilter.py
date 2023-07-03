import numpy as np
from scipy import signal
import threading
import time

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
    
    def threadRunner(self):
        while True:
            if self.STOP: return
            if len(self.buffer) == 0:
                time.sleep(0.1)
                continue
            samples = self.buffer.pop(0)
            filtered = self.run(samples)
            for output in self.outputs:
                output.write(filtered)
        
    def startSelf(self):
        print('Starting LowPassFilter')
        self.STOP = False
        self.thread = threading.Thread(target=self.threadRunner)
        self.thread.start()

    def stopSelf(self):
        print('Stopping LowPassFilter')
        self.STOP = True
        self.thread.join()
        
        
