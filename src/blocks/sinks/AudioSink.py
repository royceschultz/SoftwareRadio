import sounddevice as sd
import numpy as np

from ..BaseBlock import BaseBlock

class AudioSink(BaseBlock):
    def __init__(self):
        BaseBlock.__init__(self)
        self.block_size = 1024
        self.n_channels = 1
        self.device_id = 1

        self.stream = sd.OutputStream(
            samplerate=48000.0, blocksize=self.block_size,
            device=self.device_id, channels=self.n_channels,
            callback=self.callback,
            dtype='float32'
        )

    def addOutput(self, output):
        # Overwrite BaseBlock.addOutput
        # AudioSink does not have outputs
        raise Exception('AudioSink does not have outputs')

    def callback(self, outdata, frames, time, status):
        if len(self.buffer) == 0:
            print('underflow')
            outdata.fill(0)
            return
        outdata[:, 0] = self.buffer.pop(0)
    
    def startSelf(self):
        print('Starting AudioSink')
        self.stream.start()
    
    def stopSelf(self):
        print('Stopping AudioSink')
        self.stream.stop()
