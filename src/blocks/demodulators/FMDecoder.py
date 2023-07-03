import time
import threading
import numpy as np
from scipy import signal

from ..BaseBlock import BaseBlock

# De-emphasis filter parameters
bz, az = signal.bilinear(1, [75e-6, 1], fs=48e3)

class FMDecoder(BaseBlock):
    def __init__(self, offset_frequency=0):
        BaseBlock.__init__(self)
        self.STOP = False
        self.thread = None
        self.offset_frequency = offset_frequency

    def run(self, samples):
        dtheta = np.angle(samples[1:] * np.conj(samples[:-1]))
        return dtheta

    def decode(self):
        while True:
            if self.STOP: return
            if len(self.buffer) == 0:
                time.sleep(0.1)
                continue
            samples = self.buffer.pop(0)
            demodulated = self.run(samples)
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
