import numpy as np

from blocks.BaseBlock import BaseBlock

class MMSync(BaseBlock):
    def __init__(self):
        BaseBlock.__init__(self)

    def run(self, samples):

        bps = 1187.5  # bits per second
        samp_rate = 24e5 / 10
        sps = samp_rate / bps  # samples per symbol

        # Muller and Mueller Clock Recovery
        # I have no idea how this works, but it does
        # Thanks Marc Lichtman - https://pysdr.org/content/sync.html
        mu = 0  # initial estimate of phase of sample
        out = np.zeros(len(samples) + 10, dtype=samples.dtype)
        # stores values, each iteration we need the previous 2 values plus current value
        out_rail = np.zeros(len(samples) + 10, dtype=samples.dtype)
        i_in = 0  # input samples index
        i_out = 2  # output index (let first two outputs be 0)
        roots = []
        while i_out < len(samples) and i_in+16 < len(samples):
            # grab what we think is the "best" sample
            idx = i_in + int(mu)
            roots.append(idx)
            out[i_out] = samples[idx]
            out_rail[i_out] = int(np.real(out[i_out]) > 0) + \
                1j*int(np.imag(out[i_out]) > 0)
            x = (out_rail[i_out] - out_rail[i_out-2]) * np.conj(out[i_out-1])
            y = (out[i_out] - out[i_out-2]) * np.conj(out_rail[i_out-1])
            mm_val = np.real(y - x)
            mu += sps + 0.3*mm_val
            # round down to nearest int since we are using it as an index
            i_in += int(np.floor(mu))
            mu = mu - np.floor(mu)  # remove the integer part of mu
            i_out += 1  # increment output index
        # remove the first two, and anything after i_out (that was never filled out)
        out = out[2:i_out]
        roots = np.array(roots)

        return out
