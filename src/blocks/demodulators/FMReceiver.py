from ..misc.Sequential import Sequential
from ..filters.LowPassFilter import LowPassFilter
from ..filters.Decimate import Decimate
from .FMDecoder import FMDecoder
from ..filters.FMDemphasis import FMDemphasis

def FMReceiver(sample_rate=24e5, cutoff_frequency=100e3, transition_width=100e3, decimation_factor=50):
    return Sequential(
        LowPassFilter(sample_rate=sample_rate, cutoff_frequency=cutoff_frequency, transition_width=transition_width),
        FMDecoder(),
        Decimate(decimation_factor=decimation_factor),
        FMDemphasis()
    )
