from blocks import SignalSource, AudioSink, FMReceiver

source = SignalSource(block_size=1024 * 50)

fmClient = FMReceiver()
sink = AudioSink()

source.addOutput(fmClient)
fmClient.addOutput(sink)

source.start(recursive=True)

input('Press enter to stop\n')

source.stop(recursive=True)
