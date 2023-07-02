from blocks.SignalSource import SignalSource
from blocks.FMDecoder import FMDecoder
from blocks.AudioSink import AudioSink

source = SignalSource()
decoder = FMDecoder()
sink = AudioSink()

decoder2 = FMDecoder(offset_frequency=-400e3)
sink2 = AudioSink()

source.addOutput(decoder)
decoder.addOutput(sink)

source.addOutput(decoder2)
decoder2.addOutput(sink2)

source.start(recursive=True)

input('Press enter to stop\n')
decoder.stop(recursive=True)
input()
decoder2.stop(recursive=True)
decoder.start(recursive=True)
input()

source.stop(recursive=True)
