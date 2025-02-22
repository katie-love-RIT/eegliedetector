
import argparse
from brainflow.board_shim import BoardShim, BoardIds

def get_sampling_rate(board):
    sampling_rate = board.get_sampling_rate(BoardIds.SYNTHETIC_BOARD.value)
    print(Sampling Rate:, sampling_rate)
    return sampling_rate

