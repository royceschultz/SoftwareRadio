from blocks import Sequential, LowPassFilter, Decimate, MMSync
from blocks.BaseBlock import BaseBlock
from .MMSync import MMSync
from .Symbols import Symbols

class RDSReceiver(BaseBlock):
    def __init__(self, sample_rate=48e3):
        BaseBlock.__init__(self)
        self.decimation_factor = 5
        self.decimate = Decimate(decimation_factor=self.decimation_factor)
        self.low_pass = LowPassFilter(sample_rate=sample_rate / self.decimation_factor, cutoff_frequency=5e3,
                                      transition_width=3e3, offset_frequency=57e3)
        
        mmsync = MMSync()
        self.seq = Sequential(
            Decimate(decimation_factor=2),
            mmsync,
            Symbols()
        )

        self.decimate.addOutput(self.low_pass)
        self.low_pass.addOutput(self.seq)
    
    def write(self, samples):
        self.decimate.write(samples)

    def startSelf(self):
        self.decimate.start(recursive=True)
        # self.symbols.start(recursive=True)

    def stopSelf(self):
        self.decimate.stop(recursive=True)
        # self.symbols.stop(recursive=True)

# def RDSReceiver(sample_rate=48e3):
#     decimation_factor = 10
#     decimate = Decimate(decimation_factor=decimation_factor)
#     low_pass = LowPassFilter(sample_rate=sample_rate / decimation_factor, cutoff_frequency=5e3,
#                                 transition_width=5e3, offset_frequency=57e3)
#     seq = Sequential(
#         MMSync(),
#     )

#     decimate.addOutput(low_pass)
#     low_pass.addOutput(seq)
#     return decimate
