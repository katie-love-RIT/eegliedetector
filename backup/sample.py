import argparse
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
import numpy as np
import rand as random

def init_board():
    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()
    params.ip_port = 0
    params.serial_port = "/dev/ttyUSB0"
    board = BoardShim(0, params)
    return board

def get_channels(board):
    eeg_channels = board.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
    print("EEG Channels:", eeg_channels)
    return eeg_channels

def get_sampling_rate(board):
    sampling_rate = board.get_sampling_rate(BoardIds.SYNTHETIC_BOARD.value)
    print("Sampling Rate:", sampling_rate)
    return sampling_rate

def preprocess(eeg_channels, data, sampling_rate): 
    for channel in eeg_channels:
       DataFilter.perform_bandpass(data[channel], sampling_rate, 0.1, 30.0, 4, FilterTypes.BUTTERWORTH.value, 0)
    return data

"""
event markers logic:
0 seconds: start
5 seconds (enough time to relax and get ready for stimulus): Question 1
10 seconds: Question 2
15 seconds: Question 3
we need to time their answers with a timer
"""

"""
    Extracts the P300 component from EEG data using real event markers.
    
    :param eeg_channels: List of EEG channel indices
    :param data: EEG data array (channels x samples)
    :param event_markers: List of event timestamps (sample indices)
    :param sampling_rate: Sampling rate of EEG device
    :return: Averaged P300 waveform
"""

def extract_p300_real(eeg_channels, data, event_markers, sampling_rate):

    # PART 1: Convert from Sampling Rate to Milliseconds
    # since P300 Is measured in ms, but we have a specific sampling rate on our EEG board
    # we assume 1 second = 1 sample
    pre_stimulus_period_duration_in_samples = int(sampling_rate * 0.2)  # 200ms baseline before event
    post_stimulus_period_duration_in_samples  = int(sampling_rate * 0.8)  # 800ms post-event
    epoch_length = pre_stimulus_period_duration_in_samples + post_stimulus_period_duration_in_samples  # Total epoch length
    
    p300_responses = []
    
    for event in event_markers:
        start_index = event - pre_stimulus_period_duration_in_samples
        end_index = event + post_stimulus_period_duration_in_samples
        
        if start_idex < 0 or end_idex > data.shape[1]:  # Prevent out-of-bounds errors
            continue  

        epoch = data[eeg_channels, start_index:end_index]  # Extract EEG data for the epoch
        baseline = np.mean(epoch[:, :pre_stimulus_period_duration_in_samples], axis=1, keepdims=True)  # Baseline correction
        epoch -= baseline  
        p300_responses.append(epoch)

    if len(p300_responses) == 0:
        print("No valid P300 epochs found!")
        return None

    p300_avg = np.mean(p300_responses, axis=0)  # Average across trials
    return p300_avg

def decide_card():
    choices = ['laser cutter', 'blowtorch', 'giant drill', 'car', 'oversized key', 'rocket-powered ram']
    your_number = random.randint(0,5)

your_card = decide_card()

def main():
    # start the board, get EEG channels, get sampling rate
    board = init_board()
    eeg_channels = get_channels(board)
    sampling_rate = get_sampling_rate(board)
    event_markers = [i * 5 for i in range(0, 10)]

    # start streaming
    board.prepare_session()
    board.start_stream()

    # wait 10 seconds
    time.sleep(2)

    # gets the data; answers the question what is on the channels right now? 
    # 'get all data and remove it from internal buffer'
    # returns an array, 1 row for each channel & each column is a data point 
    # each entry is a coefficient of a sine wave (we think)
    # the number of data pts
    data = board.get_board_data() 
    print("Unfiltered: ", data)
    filtered_data = preprocess(eeg_channels, data, sampling_rate)

    # stop stream 
    board.stop_stream()
    board.release_session()
    print("filtered: ", filtered_data)


if __name__ == "__main__":
    main()