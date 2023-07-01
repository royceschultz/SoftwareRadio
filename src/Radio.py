from rtlsdr import *
from pylab import *
from scipy import signal

import RadioHelpers as rh

sdr = RtlSdr()

# configure device
samp_rate = 24e5
sdr.sample_rate = samp_rate
sdr.center_freq = 93.3e6
sdr.gain = 20

nyq_rate = samp_rate / 2.0
w = rh.kilohertz(100) / nyq_rate
c = rh.kilohertz(100) / nyq_rate
attenuation = 60.0

# Filters
N, beta = signal.kaiserord(attenuation, w)
taps = signal.firwin(N, c, window=('kaiser', beta))

bz, az = signal.bilinear(1, [75e-6, 1], fs=48e3)

def getSDR():
    return sdr

def setFrequency(freq):
    sdr.center_freq = freq

def collect(n_samples):
    samples = sdr.read_samples(n_samples * 50)
    return samples

def demod(samples):
    filtered = signal.lfilter(taps, 1.0, samples)
    dtheta = np.angle(filtered[1:] * np.conj(filtered[:-1]))
    decimated = dtheta[::50] # decimate
    filtered_fm_signal = signal.lfilter(bz, az, decimated)
    return filtered_fm_signal
