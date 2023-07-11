from blocks import Sequential, RDSReceiver, LowPassFilter, LowPassFilter, Decimate, FMDemphasis, FMDecoder
from blocks.BaseBlock import BaseBlock

class FMReceiver(BaseBlock):
    def __init__(self, sample_rate=24e5, cutoff_frequency=100e3, transition_width=100e3, decimation_factor=50):
        BaseBlock.__init__(self)
        self.rds_client = RDSReceiver(sample_rate=sample_rate)

        quad_decode = FMDecoder()
        quad_decode.addOutput(self.rds_client)

        self.seq = Sequential(
            LowPassFilter(sample_rate=sample_rate, cutoff_frequency=cutoff_frequency,
                        transition_width=transition_width),
            quad_decode,
            Decimate(decimation_factor=decimation_factor),
            FMDemphasis()
        )

    def run(self, samples):
        return self.seq.run(samples)
    
    def write(self, samples):
        self.seq.write(samples)

    def startSelf(self):
        self.seq.start(recursive=True)
        self.rds_client.start(recursive=True)

    def stopSelf(self):
        self.seq.stop(recursive=True)
        self.rds_client.stop(recursive=True)

    def addOutput(self, output):
        return self.seq.addOutput(output)
