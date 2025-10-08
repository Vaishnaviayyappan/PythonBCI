# config.py

# --- BrainFlow Settings ---
# For a list of available boards, see: https://brainflow.readthedocs.io/en/stable/SupportedBoards.html
BOARD_ID = 38  # 38 = Muse 2, 2 = Muse 2016, 1 = OpenBCI Cyton, etc.
SERIAL_PORT = "" # Not needed for Muse (uses Bluetooth)
IP_ADDRESS = ""   # Not needed for Muse
MAC_ADDRESS = ""  # Optional: can help connect to a specific Muse device

# --- EEG Channel Settings ---
# The Muse has 5 channels (TP9, AF7, AF8, TP9, AUX)
# We are interested in the visual cortex, so AF7 and AF8 are good choices.
# Channels are indexed starting from 0. (e.g., 0=TP9, 1=AF7, 2=AF8, 3=TP10, 4=AUX)
EEG_CHANNELS = [1, 2] # Use AF7 and AF8 channels

# --- SSVEP Frequencies ---
# Each key is assigned a unique flickering frequency.
KEY_FREQUENCIES = {
    'A': 6.0, 'B': 6.5, 'C': 7.0, 'D': 7.5, 'E': 8.0,
    'F': 8.5, 'G': 9.0, 'H': 9.5, 'I': 10.0, 'J': 10.5,
    'K': 11.0, 'L': 11.5, 'M': 12.0, '<': 8.2, ' ': 10.2 # < for Backspace, ' ' for Space
}

# --- SSVEP Processing Settings ---
SAMPLING_RATE = 256 # Muse 2's sampling rate
WINDOW_LENGTH = 2   # seconds of data to analyze at a time
PREDICTION_THRESHOLD = 0.5 # Confidence threshold for a selection
