import numpy as np

from blocks.BaseBlock import BaseBlock


class Symbols(BaseBlock):
    def __init__(self):
        BaseBlock.__init__(self)

    def run(self, samples):
        square = samples ** 2
        avg_angle = np.angle(square).mean()
        # rotate samples by -avg_angle
        post_samples = samples * np.exp(-1j * avg_angle / 2)
        bits = np.zeros(len(post_samples), dtype=np.int8)
        bits[post_samples.real > 0] = 1

        bits = np.abs(np.diff(bits)) # differential encoding
        print(''.join(map(str, bits)))

        return bits
