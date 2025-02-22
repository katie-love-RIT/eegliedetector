
from brainflow.data_filter import DataFilter, FilterTypes

def preprocess(eeg_channels, data, sampling_rate): 
    for channel in eeg_channels:
        DataFilter.perform_bandpass(data[channel], sampling_rate, 0.1, 30.0, 4, FilterTypes.BUTTERWORTH.value, 0)
    return data

