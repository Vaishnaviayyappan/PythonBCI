# PythonBCI

EEG Virtual Keyboard using Brain-Computer Interface
A real-time Brain-Computer Interface (BCI) application that allows you to type using your brainwaves. This project uses Steady-State Visually Evoked Potentials (SSVEP) to detect which key you're looking at on a virtual keyboard.

🧠 How It Works
This application uses a scientifically validated BCI paradigm called SSVEP (Steady-State Visually Evoked Potential):

Visual Stimulation: Each key on the virtual keyboard flickers at a unique frequency (e.g., 'A' at 6 Hz, 'B' at 6.5 Hz).
Brain Response: When you look at a flickering key, your visual cortex generates electrical activity at that same frequency.
Signal Detection: The EEG headset records your brainwaves, and our algorithm detects which frequency is strongest.
Character Selection: The system identifies which key you're focusing on and types the corresponding character.

✨ Features

Real EEG Hardware Integration: Connects to actual EEG devices via BrainFlow
SSVEP-based Selection: Uses a scientifically proven BCI paradigm
Real-time Processing: Analyzes brain signals in real-time
Visual Feedback: Flickering keyboard with typed text display
Multiple Device Support: Compatible with Muse, OpenBCI, and other BrainFlow-supported devices
Configurable: Easy-to-modify settings for frequencies, channels, and thresholds

🔧 Hardware Requirements
Supported EEG Devices
This project works with any EEG device supported by BrainFlow, including:

Muse 2 or Muse S (Recommended for beginners - ~$250)
OpenBCI Cyton or Ganglion (~$200-500)
Emotiv EPOC+ (~$800)
NeuroSky MindWave (~$100)
And many more...

Computer Requirements

Bluetooth: Built-in or USB Bluetooth adapter
Operating System: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
RAM: 4GB minimum, 8GB recommended
Python: 3.7 or higher

📦 Software Installation
Step 1: Clone the Repository
git clone https://github.com/yourusername/eeg-virtual-keyboard.git
cd eeg-virtual-keyboard
BASH
Step 2: Create a Virtual Environment (Recommended)
Windows:
python -m venv venv
venv\Scripts\activate
BASH
macOS/Linux:
python3 -m venv venv
source venv/bin/activate
BASH
Step 3: Install Dependencies
pip install brainflow pygame numpy scipy pyserial
BASH
⚙️ Configuration
Before running the application, you need to configure it for your specific EEG device.
1. Find Your Board ID
Open config.py and set the BOARD_ID for your device:
# Common Board IDs:
# 38 = Muse 2
# 2  = Muse 2016
# 1  = OpenBCI Cyton
# 3  = OpenBCI Ganglion
# 21 = NeuroSky MindWave

BOARD_ID = 38  # Change this to match your device
PYTHON
See the full list of Board IDs.
2. Configure Device Connection
For Muse 2/S (Bluetooth):

Find your Muse's MAC address:
Windows:

Go to Settings → Bluetooth & other devices
Click on your paired Muse device → Properties
Note the address (e.g., 00:55:DA:B0:12:34)

macOS:
system_profiler SPBluetoothDataType | grep "Muse"
BASH
Linux:

bluetoothctl
devices
BASH
Update config.py:

MAC_ADDRESS = "00:55:DA:B0:12:34"  # Your Muse's MAC address
PYTHON
For OpenBCI (Serial/WiFi):
SERIAL_PORT = "COM3"  # Windows: COM3, COM4, etc.
# or
SERIAL_PORT = "/dev/ttyUSB0"  # Linux
# or
IP_ADDRESS = "192.168.1.100"  # For WiFi Shield
PYTHON
3. Select EEG Channels
Different headsets have different channel layouts. Configure which channels to use:

# For Muse (5 channels: TP9, AF7, AF8, TP10, AUX)
# Indexes: 0=TP9, 1=AF7, 2=AF8, 3=TP10, 4=AUX
# AF7 and AF8 are over the visual cortex
EEG_CHANNELS = [1, 2]  # Use AF7 and AF8

# For OpenBCI Cyton (8 channels)
# Use channels over occipital region (O1, O2, Oz)
# EEG_CHANNELS = [5, 6, 7]  # Example
PYTHON
🚀 Running the Application
Step 1: Prepare Your EEG Device
Charge your EEG headset fully
Turn it on and ensure it's in pairing mode
Pair it with your computer via Bluetooth (for Muse/wireless devices)
Step 2: Test the Connection
Run the test script to verify BrainFlow can connect to your device:

python test_brainflow.py
BASH
You should see: Successfully connected to the board!

If you see an error, refer to the Troubleshooting section below.

Step 3: Run the Virtual Keyboard
python main.py
BASH
Step 4: Using the Keyboard
Put on your EEG headset and ensure good electrode contact (especially over the visual cortex)
The virtual keyboard window will appear with flickering keys
Look directly at a key you want to type
Focus on it for 2-3 seconds without moving your eyes
The system will detect your selection and type the character
There is a 3-second cooldown between selections to prevent accidental double-typing
📁 Project Structure
eeg_keyboard/
│
├── main.py              # Main application entry point
├── gui.py               # Pygame-based virtual keyboard GUI
├── bci_processor.py     # EEG data acquisition and processing logic
├── config.py            # Configuration file (device, channels, frequencies)
├── test_brainflow.py    # Connection test script
├── requirements.txt     # Python dependencies
└── README.md            # This file
BASH
🔬 Understanding the Code
config.py
Device settings: Board ID, MAC address, serial port
Channel selection: Which EEG channels to analyze
SSVEP frequencies: Each key's flicker frequency
Processing parameters: Window length, thresholds
bci_processor.py
Connection management: Connects to EEG device via BrainFlow
Data acquisition: Retrieves real-time EEG data
Signal processing: Uses Welch's method to compute Power Spectral Density (PSD)
Classification: Identifies the strongest frequency to determine which key you're looking at
gui.py
Keyboard rendering: Draws flickering keys at specific frequencies
Text display: Shows typed characters
Prediction integration: Calls the BCI processor and handles selections
main.py
Initialization: Sets up the BCI processor and GUI
Error handling: Manages connection failures gracefully
🐛 Troubleshooting
Error: BOARD_NOT_READY_ERROR
Problem: BrainFlow cannot connect to your EEG device.

Solutions:

Ensure your device is turned on and charged
Close any other apps using the device (Muse app, other BCI software)
On Windows, run the script as Administrator
Verify your MAC_ADDRESS or SERIAL_PORT in config.py is correct
Try unpairing and re-pairing your device in Bluetooth settings
Error: Key is not defined
Problem: Variable name error in the GUI code.

Solution: Make sure you're using the corrected gui.py provided in this repository.

Poor Detection / No Selections
Problem: The system isn't detecting your selections.

Solutions:

Check electrode contact: Ensure the EEG sensors are making good contact with your scalp
Reduce ambient light: Bright lights can interfere with SSVEP
Adjust threshold: Lower PREDICTION_THRESHOLD in config.py (try 0.3 instead of 0.5)
Use correct channels: Make sure EEG_CHANNELS in config.py corresponds to the visual cortex
Stay still: Minimize head movement and blinking
Flicker Frequencies Not Working
Problem: Keys don't seem to flicker at the right rate.

Solution: Ensure your monitor refresh rate is at least 60 Hz. Lower refresh rates can cause aliasing.

🔮 Future Enhancements
 User Calibration: Personalized training phase to improve accuracy
 More Keys: Support for full QWERTY keyboard layout
 Adaptive Thresholds: Automatically adjust detection sensitivity
 Multi-frequency Detection: Improve selection speed with harmonic analysis
 Word Prediction: Auto-complete based on typed context
 Filter Bank Analysis: More robust frequency detection
 Export Data: Save EEG sessions for offline analysis
📚 Scientific Background
This project is based on decades of BCI research:

SSVEP (Steady-State Visually Evoked Potential): When you look at a flickering stimulus, your brain's visual cortex produces electrical oscillations at the same frequency.
Power Spectral Density (PSD): We use Welch's method to transform time-domain EEG signals into the frequency domain.
Classification: By identifying which frequency has the highest power, we determine which key you're looking at.
Key Papers:

Bin et al. (2009) - "A high-speed BCI based on code modulation VEP"
Vialatte et al. (2010) - "Steady-state visually evoked potentials"
🤝 Contributing
Contributions are welcome! Here's how you can help:

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request


⚠️ Disclaimer
This is a research and educational project. It is not a medical device and should not be used for any clinical or diagnostic purposes. Always consult with qualified professionals for medical advice.

📧 Contact
Vaishnavi A-vaishnaviayyappan16@gmail.com

Project Link: https://github.com/yourusername/eeg-virtual-keyboard

🙏 Acknowledgments
BrainFlow - The open-source library that makes multi-device EEG integration possible
Pygame - For the graphical interface
The BCI research community for decades of foundational work
Muse, OpenBCI, and other open hardware manufacturers
