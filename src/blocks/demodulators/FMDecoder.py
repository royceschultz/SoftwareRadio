import time
import numpy as np
from scipy import signal

from ..BaseBlock import BaseBlock

# De-emphasis filter parameters
bz, az = signal.bilinear(1, [75e-6, 1], fs=48e3)

class FMDecoder(BaseBlock):
    def __init__(self, offset_frequency=0):
        BaseBlock.__init__(self)
        self.offset_frequency = offset_frequency

    def run(self, samples):
        dtheta = np.angle(samples[1:] * np.conj(samples[:-1]))
        return dtheta
