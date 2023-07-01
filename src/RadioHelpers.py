from scipy import signal

def megahertz(x):
    return 1e6 * x


def kilohertz(x):
    return 1e3 * x


def lowPassFilter(samples, sample_rate, cutoff, transition):
    nyq_rate = sample_rate / 2.0
    w = transition / nyq_rate
    c = cutoff / nyq_rate
    attenuation = 60.0
    N, beta = signal.kaiserord(attenuation, w)
    taps = signal.firwin(N, c, window=('kaiser', beta))
    return signal.lfilter(taps, 1.0, samples)
