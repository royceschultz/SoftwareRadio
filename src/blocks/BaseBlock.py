import threading
import time

class BaseBlock:
    def __init__(self):
        self.outputs = []
        self.buffer = []
        self._stop = False
        self.thread = None
        self.name = None

    def run(self, samples):
        raise Exception('run not implemented')

    def addOutput(self, output):
        self.outputs.append(output)

    def emit(self, samples):
        if not self.outputs: return
        for output in self.outputs:
            output.write(samples)

    def write(self, samples):
        if len(self.buffer) > 10:
            print('OVERFLOW', self.__class__.__name__, self.name)
            return
        self.buffer.append(samples)
        pass

    def threadRunner(self):
        while not self._stop:
            if not self.buffer:
                time.sleep(0.01)
                continue
            samples = self.buffer.pop(0)
            res = self.run(samples)
            self.emit(res)

    def startSelf(self):
        self._stop = False
        self.thread = threading.Thread(target=self.threadRunner)
        self.thread.start()

    def stopSelf(self):
        self._stop = True
        self.thread.join()

    def start(self, recursive=False):
        self.startSelf()
        if recursive:
            self.startChildren()

    def startChildren(self):
        for output in self.outputs:
            output.start(recursive=True)

    def stop(self, recursive=False):
        self.stopSelf()
        if recursive:
            self.stopChildren()
    
    def stopChildren(self):
        for output in self.outputs:
            output.stop(recursive=True)
