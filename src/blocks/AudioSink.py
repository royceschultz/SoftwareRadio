import sounddevice as sd
import numpy as np

class AudioSink:
    def __init__(self):
        self.block_size = 1024
        self.n_channels = 1
        self.device_id = 1

        self.buffer = []

        self.stream = sd.OutputStream(
            samplerate=48000.0, blocksize=self.block_size,
            device=self.device_id, channels=self.n_channels,
            callback=self.callback,
            dtype='float32'
        )


    def callback(self, outdata, frames, time, status):
        if len(self.buffer) == 0:
            print('underflow')
            outdata.fill(0)
            return
        outdata[:, 0] = self.buffer.pop(0)

    def write(self, samples):
        if len(self.buffer) > 10:
            # print('OVERFLOW - AudioSink')
            return
        self.buffer.append(samples)
    
    def start(self, recursive=False):
        print('Starting AudioSink')
        self.stream.start()
        # No outputs to start recursively
    
    def stop(self, recursive=False):
        print('Stopping AudioSink')
        self.stream.stop()
        # No outputs to stop recursively
