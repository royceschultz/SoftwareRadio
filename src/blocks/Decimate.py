from .BaseBlock import BaseBlock

class Decimate(BaseBlock):
    def __init__(self, decimation_factor=50):
        BaseBlock.__init__(self)
        self.decimation_factor = decimation_factor

    def run(self, samples):
        return samples[::self.decimation_factor]
