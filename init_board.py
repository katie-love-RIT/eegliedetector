
import argparse
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

def init_board():
    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()
    params.ip_port = 0
    params.serial_port = /dev/ttyUSB0
    board = BoardShim(0, params)
    return board

