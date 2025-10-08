# bci_processor.py

import numpy as np
from scipy.signal import welch
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels
from config import *

class BCIProcessor:
    def __init__(self):
        self.params = BrainFlowInputParams()
        self.params.serial_port = SERIAL_PORT
        self.params.ip_address = IP_ADDRESS
        self.params.mac_address = MAC_ADDRESS
        
        self.board_id = BOARD_ID
        self.board = None
        self.is_streaming = False
        
        self.target_frequencies = list(KEY_FREQUENCIES.values())
        self.keys = list(KEY_FREQUENCIES.keys())

    def connect(self):
        """Connect to the EEG board and start streaming data."""
        try:
            self.board = BoardShim(self.board_id, self.params)
            self.board.prepare_session()
            self.board.start_stream(45000, '') # Use a large buffer
            self.is_streaming = True
            print("EEG Board connected and streaming.")
            return True
        except Exception as e:
            print(f"Error connecting to board: {e}")
            print("Please ensure your device is on and paired.")
            return False

    def disconnect(self):
        """Stop streaming and release the session."""
        if self.board and self.is_streaming:
            self.board.stop_stream()
            self.board.release_session()
            self.is_streaming = False
            print("EEG Board disconnected.")

    def predict(self):
        """
        Get the latest data, process it, and return a prediction.
        Returns a tuple (predicted_key, confidence_score) or (None, 0).
        """
        if not self.is_streaming:
            return None, 0

        # Get the last `WINDOW_LENGTH` seconds of data
        data = self.board.get_current_board_data(WINDOW_LENGTH * SAMPLING_RATE)
        eeg_data = data[EEG_CHANNELS, :]

        if eeg_data.shape[1] < (WINDOW_LENGTH * SAMPLING_RATE * 0.8): # Not enough data
            return None, 0

        # --- Signal Processing ---
        # 1. Average the selected channels
        avg_eeg = np.mean(eeg_data, axis=0)
        
        # 2. Calculate the Power Spectral Density (PSD) using Welch's method
        freqs, psd = welch(avg_eeg, fs=SAMPLING_RATE, nperseg=SAMPLING_RATE)
        
        # 3. Find the PSD values at our target frequencies
        psd_values = []
        for freq in self.target_frequencies:
            idx = np.argmin(np.abs(freqs - freq))
            psd_values.append(psd[idx])
        
        # 4. Make a prediction
        if not psd_values:
            return None, 0
            
        psd_values = np.array(psd_values)
        max_psd_index = np.argmax(psd_values)
        confidence = psd_values[max_psd_index] / np.sum(psd_values) if np.sum(psd_values) > 0 else 0
        
        if confidence > PREDICTION_THRESHOLD:
            predicted_key = self.keys[max_psd_index]
            return predicted_key, confidence
        else:
            return None, 0
