from brainflow.board_shim import BrainFlowInputParams, BoardShim, BoardIds
import numpy as np
import time



BoardShim.enable_dev_board_logger()
params = BrainFlowInputParams()
params.serial_port = "/dev/ttyUSB0"
board = BoardShim(BoardIds.CYTON_BOARD.value, params)
board.prepare_session()
board.start_stream()
time.sleep(5)  # Wait for data to accumulate
data = board.get_board_data()
board.stop_stream()
board.release_session()
print(data)