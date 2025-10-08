# main.py

import pygame
from bci_processor import BCIProcessor
from gui import VirtualKeyboardGUI
import brainflow
from config import BOARD_ID

# Set BrainFlow log level to reduce console noise
brainflow.board_shim.BoardShim.set_log_level(brainflow.board_shim.LogLevels.LEVEL_ERROR)

def main():
    processor = BCIProcessor()
    gui = VirtualKeyboardGUI(processor)

    print("Attempting to connect to EEG device...")
    if processor.connect():
        print("Starting GUI...")
        gui.run()
    else:
        print("Could not connect. Exiting.")

if __name__ == "__main__":
    main()
