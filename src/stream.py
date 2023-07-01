import sounddevice as sd
import numpy as np
import threading
import time

import Radio

devices = sd.query_devices()

# Find device index for MacBook Air Speakers
device_idx = None
for i in range(len(devices)):
    if devices[i]['name'] == 'MacBook Air Speakers':
        print(devices[i])
        device_idx = devices[i]['index']

samples_collection = []
buffer = []
STOP = False

def listen():
    while True:
        if STOP: return
        samples = Radio.collect(1024)
        samples_collection.append(samples)

def decode():
    while True:
        if STOP: return
        if (len(samples_collection) == 0):
            time.sleep(0.1)
            # print('sleeping')
            continue
        sample = samples_collection.pop(0)
        buffer.append(Radio.demod(sample))

def callback(outdata, frames, time, status):
    if len(buffer) == 0:
        print('underflow')
        outdata.fill(0)
        return
    outdata[:, 0] = buffer.pop(0)

stream = sd.OutputStream(
    samplerate=48000.0, blocksize=1024,
    device=1, channels=1,
    callback=callback, 
    dtype='float32'
)

listener = threading.Thread(target=listen)
listener.start()

decoder = threading.Thread(target=decode)
decoder.start()

stream.start()
print('started')

input()
Radio.setFrequency(94.7e6)
input()
print('stopping...')
stream.stop()
stream.close()
STOP = True
listener.join()
decoder.join()
print('stopped')
