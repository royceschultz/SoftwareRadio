import time
import threading
import numpy as np

from .BaseBlock import BaseBlock


class AMDecoder(BaseBlock):
    def __init__(self):
        BaseBlock.__init__(self)
        self.STOP = False
        self.thread = None

    def run(self, samples):
        return np.abs(samples)

    def decode(self):
        while True:
            if self.STOP:
                return
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
