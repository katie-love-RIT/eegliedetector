
import numpy as np

def extract_p300_real(eeg_channels, data, event_markers, sampling_rate):
    pre_stimulus_period_duration_in_samples = int(sampling_rate * 0.2)  # 200ms baseline before event
    post_stimulus_period_duration_in_samples = int(sampling_rate * 0.8)  # 800ms post-event
    epoch_length = pre_stimulus_period_duration_in_samples + post_stimulus_period_duration_in_samples  # Total epoch length
    
    p300_responses = []
    
    for event in event_markers:
        start_index = event - pre_stimulus_period_duration_in_samples
        end_index = event + post_stimulus_period_duration_in_samples
        
        if start_index < 0 or end_index > data.shape[1]:  # Prevent out-of-bounds errors
            continue  

        epoch = data[eeg_channels, start_index:end_index]  # Extract EEG data for the epoch
        baseline = np.mean(epoch[:, :pre_stimulus_period_duration_in_samples], axis=1, keepdims=True)  # Baseline correction
        epoch -= baseline  
        p300_responses.append(epoch)

    if len(p300_responses) == 0:
        print(No valid P300 epochs found!)
        return None

    p300_avg = np.mean(p300_responses, axis=0)  # Average across trials
    return p300_avg

