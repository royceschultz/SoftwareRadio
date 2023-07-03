from ..BaseBlock import BaseBlock
from scipy import signal

# De-emphasis filter parameters
bz, az = signal.bilinear(1, [75e-6, 1], fs=48e3)

class FMDemphasis(BaseBlock):
    def __init__(self):
        BaseBlock.__init__(self)

    def run(self, samples):
        filtered_fm_signal = signal.lfilter(bz, az, samples)
        return filtered_fm_signal
