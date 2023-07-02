class BaseBlock:
    def __init__(self):
        self.outputs = []
        self.buffer = []

    def addOutput(self, output):
        self.outputs.append(output)

    def write(self, samples):
        if len(self.buffer) > 10:
            # print('OVERFLOW - FMDecoder')
            return
        self.buffer.append(samples)
        pass

    def startSelf(self):
        raise Exception('startSelf not implemented')

    def stopSelf(self):
        raise Exception('stopSelf not implemented')

    def start(self, recursive=False):
        self.startSelf()
        if recursive:
            for output in self.outputs:
                output.start(recursive=True)

    def stop(self, recursive=False):
        self.stopSelf()
        if recursive:
            for output in self.outputs:
                output.stop(recursive=True)
