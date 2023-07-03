from .BaseBlock import BaseBlock
import threading
import time

class Sequential(BaseBlock):
    def __init__(self, *blocks):
        BaseBlock.__init__(self)
        self.blocks = blocks
        self.STOP = False
        self.thread = None

        self.name = 'Sequential: ' + str([type(b) for b in self.blocks])

    def run(self, samples):
        for block in self.blocks:
            samples = block.run(samples)
        return samples

    def threadRunner(self):
        while True:
            if self.STOP: return
            if len(self.buffer) == 0:
                time.sleep(0.1)
                continue
            samples = self.buffer.pop(0)
            samples = self.run(samples)
            for output in self.outputs:
                output.write(samples)
    
    def startSelf(self):
        print('Starting ' + self.name)
        self.STOP = False
        self.thread = threading.Thread(target=self.threadRunner)
        self.thread.start()

    def stopSelf(self):
        print('Stopping ' + self.name)
        self.STOP = True
        self.thread.join()
