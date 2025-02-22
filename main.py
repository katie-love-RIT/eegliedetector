
import time
import numpy as np
from brainflow.board_shim import BoardShim, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
from init_board import init_board
from get_channels import get_channels
from get_sampling_rate import get_sampling_rate
from preprocess import preprocess
from extract_p300_real import extract_p300_real
from decide_card import decide_card

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
    data = board.get_board_data() 
    print('Unfiltered:', data)
    filtered_data = preprocess(eeg_channels, data, sampling_rate)

    # stop stream 
    board.stop_stream()
    board.release_session()
    print('filtered:' , filtered_data)

if __name__ == __main__:
    main()

