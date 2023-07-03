from blocks import SignalSource, \
    LowPassFilter, Decimate, \
    FMDecoder, FMDemphasis, AudioSink, Sequential

source = SignalSource(block_size=1024 * 50)
lowPass = LowPassFilter(sample_rate=24e5, cutoff_frequency=100e3, transition_width=100e3)
decoder = FMDecoder()
decimate = Decimate(decimation_factor=50)
demphasis = FMDemphasis()
sink = AudioSink()

fmDemodSequence = Sequential(lowPass, decoder, decimate, demphasis)

source.addOutput(fmDemodSequence)
fmDemodSequence.addOutput(sink)

source.start(recursive=True)

input('Press enter to stop\n')

source.stop(recursive=True)
