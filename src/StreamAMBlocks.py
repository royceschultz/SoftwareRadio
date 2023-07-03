from blocks.SignalSource import SignalSource
from blocks.AMDecoder import AMDecoder
from blocks.LowPassFilter import LowPassFilter
from blocks.AudioSink import AudioSink
from blocks.Sequential import Sequential
from blocks.Decimate import Decimate

source = SignalSource(block_size=1024 * 50)
lowPass = LowPassFilter(sample_rate=24e5, cutoff_frequency=5e3, transition_width=20e3)
decimate = Decimate(decimation_factor=50)
decoder = AMDecoder()
sink = AudioSink()

amDemodSequence = Sequential(lowPass, decimate, decoder)

source.addOutput(amDemodSequence)
amDemodSequence.addOutput(sink)

source.setFrequency(126.250e6)

source.start(recursive=True)
input('Press enter to stop\n')
source.stop(recursive=True)
