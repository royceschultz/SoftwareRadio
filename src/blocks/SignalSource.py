from rtlsdr import *
import threading

from .BaseBlock import BaseBlock


class SignalSource(BaseBlock):
    def __init__(self, block_size=1024):
        BaseBlock.__init__(self)
        self.sdr = RtlSdr()
        self.sdr.sample_rate = 24e5
        self.sdr.center_freq = 93.3e6
        self.sdr.gain = 20
        self.sdr.gain = 'auto'

        self.STOP = False
        self.block_size = block_size
        self.thread = None
        pass

    def setFrequency(self, freq):
        self.sdr.center_freq = freq

    def startSelf(self):
        print('Starting SignalSource')
        self.STOP = False
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()

    def stopSelf(self):
        print('Stopping SignalSource')
        self.STOP = True
        self.thread.join()

    def listen(self):
        while True:
            if self.STOP: return
            samples = self.sdr.read_samples(self.block_size * 50)
            for output in self.outputs:
                output.write(samples)
