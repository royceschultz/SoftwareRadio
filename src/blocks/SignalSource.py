from rtlsdr import *
import threading


class SignalSource:
    def __init__(self, block_size=1024):
        self.sdr = RtlSdr()
        self.sdr.sample_rate = 24e5
        self.sdr.center_freq = 93.3e6
        self.sdr.gain = 20

        self.outputs = []
        self.STOP = False
        self.block_size = block_size
        self.thread = None
        pass

    def setFrequency(self, freq):
        self.sdr.center_freq = freq

    def addOutput(self, output):
        self.outputs.append(output)
        pass

    def start(self, recursive=False):
        print('Starting SignalSource')
        self.STOP = False
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()
        if recursive:
            for output in self.outputs:
                output.start(recursive=True)
        pass

    def stop(self, recursive=False):
        print('Stopping SignalSource')
        self.STOP = True
        self.thread.join()
        if recursive:
            for output in self.outputs:
                output.stop(recursive=True)

    def listen(self):
        while True:
            if self.STOP: return
            samples = self.sdr.read_samples(self.block_size * 50)
            for output in self.outputs:
                output.write(samples)
            pass
