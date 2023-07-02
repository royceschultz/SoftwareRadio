import time
import threading
import numpy as np
from scipy import signal

from .BaseBlock import BaseBlock


# Filter Settings
samp_rate = 24e5
nyq_rate = samp_rate / 2.0
w = 100e3 / nyq_rate
c = 100e3 / nyq_rate
attenuation = 60.0

# Filters
# Low pass filter
N, beta = signal.kaiserord(attenuation, w)
taps = signal.firwin(N, c, window=('kaiser', beta))
# De-emphasis filter
bz, az = signal.bilinear(1, [75e-6, 1], fs=48e3)

def demodFM(
        samples, offsetFrequency=0,
        samp_rate=24e5,):
    if offsetFrequency != 0:
        w = -1.0j * 2.0 * np.pi * \
            (offsetFrequency / samp_rate) * np.arange(len(samples))
        samples = samples * np.exp(w)
    # Low pass filter
    filtered = signal.lfilter(taps, 1.0, samples)
    # Calculate phase difference
    dtheta = np.angle(filtered[1:] * np.conj(filtered[:-1]))
    # Decimate
    decimated = dtheta[::50]
    # De-emphasis filter
    filtered_fm_signal = signal.lfilter(bz, az, decimated)
    return filtered_fm_signal


class FMDecoder(BaseBlock):
    def __init__(self, offset_frequency=0):
        BaseBlock.__init__(self)
        self.STOP = False
        self.thread = None
        self.offset_frequency = offset_frequency

    def decode(self):
        while True:
            if self.STOP: return
            if len(self.buffer) == 0:
                time.sleep(0.1)
                continue
            samples = self.buffer.pop(0)
            demodulated = demodFM(samples, offsetFrequency=self.offset_frequency)
            for output in self.outputs:
                output.write(demodulated)

    def startSelf(self):
        print('Starting FMDecoder')
        self.STOP = False
        self.thread = threading.Thread(target=self.decode)
        self.thread.start()
    
    def stopSelf(self):
        print('Stopping FMDecoder')
        self.STOP = True
        self.thread.join()