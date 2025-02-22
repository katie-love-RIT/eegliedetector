
import argparse
from brainflow.board_shim import BoardShim, BoardIds

def get_channels(board):
    eeg_channels = board.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
    print(EEG Channels:, eeg_channels)
    return eeg_channels

