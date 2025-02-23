
import time
import cv2
import numpy as np
import random
from brainflow.board_shim import BoardShim, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes
from init_board import init_board
from get_channels import get_channels
from get_sampling_rate import get_sampling_rate
from preprocess import preprocess
from extract_p300_real import extract_p300_real
from decide_card import decide_card

global channel_dict 
channel_dict = {
        1: "Right Occipital (O2)",
        2: "Left Central (C3)",
        3: "Right Parietal (P4)",
        4: "Right Central (C4)",
        5: "Central Midline (CZ)",
        6: "Parietal Midline (Pz)",
        7: "Left Parietal (P3)",
        8: "Left Occipital (O1)"
    }

global board 

def slideshow():
    # decide which you used
    choices = ['boltcutters.jpg', 'blowtorch.jpg', 'drill.webp', 'flamethrower.jpeg', 'stethoscope.webp', 'dynamite.jpeg', 'magnet.jpg', 'magicwand.webp', 'button.jpg']


def main(): 
    # start the board, get EEG channels, get sampling rate
    board = init_board()
    eeg_channels = get_channels(board)
    sampling_rate = get_sampling_rate(board)
    
    # start streaming
    board.prepare_session()
    board.start_stream(250)

    # decide which you used
    choices = ['boltcutters.jpg', 'blowtorch.jpg', 'drill.webp', 'flamethrower.jpeg', 'stethoscope.webp', 'dynamite.jpeg', 'magnet.jpg', 'magicwand.webp', 'button.jpg']

    your_number = random.randint(0,len(choices)-1)
    your_choice = choices[your_number]

    # Load the image  
    image = cv2.imread(your_choice)  

    time.sleep(1)

    baseline_peaks_before_stimulus = get_max_microvolts_per_brain_area(board, eeg_channels, sampling_rate, 300)

    # Show the image  
    cv2.imshow('Image', image)  

    #time.sleep(.6)

    # Wait for 1 second  
    cv2.waitKey(3000)  

    image = cv2.imread(choices[random.randint(0,len(choices)-1))  

    cv2.imshow('Image', image)  

    cv2.waitKey(3000)  

    # Close the image window  
    cv2.destroyAllWindows()  

    peaks_after_stimulus = get_max_microvolts_per_brain_area(board, eeg_channels, sampling_rate, 600)

    for (channel_before, peak_before), (channel_after, peak_after) in zip(
        baseline_peaks_before_stimulus.items(), peaks_after_stimulus.items()
    ):
        difference = peak_after - peak_before
        print(difference)



def get_max_microvolts_per_brain_area(board, eeg_channels, sampling_rate, time_measured_in_ms=1000):

    #what is on the channels right now? 

    data = board.get_board_data(int(time_measured_in_ms/4))

    # 250/4 = 62.5 = number of samples taken in 250ms 
    # board.get_board_data(62) = the last 62 samples taken (therefore the last ~250ms)

    final_results = {}

    filtered_data = preprocess(eeg_channels, data, sampling_rate)
    
    for i in range(1,9):
        brain_area = channel_dict[i]
        max_microvolt_for_this_channel = data[i].max()
        final_results[brain_area] = float(max_microvolt_for_this_channel)

    for result in final_results.items():
        print(result)

    print('\n')
    return final_results

# #300ms before stimulus:
# #this will run WHEN STIMULUS is shown
# baseline_peaks_before_stimulus = get_max_microvolts_per_brain_area(board, eeg_channels, sampling_rate, 300)

# #600ms after stimulus:
# # this will run 600ms after stimulus 
# peaks_after_stimulus = get_max_microvolts_per_brain_area(board, eeg_channels, sampling_rate, 600)

# baseline_peaks_before_stimulus - peaks_after_stimulus = difference

# get_max_microvolts_per_brain_area(2)

if __name__ == '__main__':
    main()

