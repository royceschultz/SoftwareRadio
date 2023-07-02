from blocks.SignalSource import SignalSource
from blocks.TransmissionDetector import TransmissionDetector

source = SignalSource()
detector = TransmissionDetector()

source.addOutput(detector)
source.setFrequency(123.85e6)

source.start(recursive=True)

input('Press enter to stop\n')

source.stop(recursive=True)
