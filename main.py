import pygame
import numpy as np
import random
import time
from sklearn.svm import SVC # Support Vector Classifier
from sklearn.preprocessing import StandardScaler
import pickle

# --- 1. Simulated BCI Data Acquisition ---
# In a real application, this would connect to an EEG headset's SDK.
class SimulatedEEG:
    """
    Simulates an EEG data stream.
    In a real-world scenario, this class would interface with hardware.
    """
    def get_data(self):
        """
        Generates a random data point.
        For a real BCI, this would be a multi-dimensional array of brain wave data.
        """
        # Simulate 8 channels of EEG data
        return np.random.rand(8)

# --- 2. Machine Learning Model ---
# This is the "brain" of the BCI. It learns to associate brain patterns with commands.
class BCIModel:
    def __init__(self):
        self.scaler = StandardScaler()
        # Using a simple Support Vector Classifier
        self.classifier = SVC(kernel='linear', probability=True)
        self.is_trained = False
        self._train_model() # For simulation, we train it immediately

    def _train_model(self):
        """
        In a real project, you would collect training data from the user.
        The user would focus on each key, and you would record the EEG signal
        at that moment, labeling it with the corresponding key.
        """
        print("Training BCI model...")
        # --- SIMULATED TRAINING DATA ---
        # We create fake data to train our model.
        # 'no_action' data is random.
        # 'select' data is slightly different.
        num_samples = 200
        features = 8 # Number of EEG channels
        
        no_action_data = np.random.randn(num_samples, features)
        select_data = np.random.randn(num_samples, features) + 0.5 # Biased data
        
        X = np.vstack((no_action_data, select_data))
        y = np.array(['no_action'] * num_samples + ['select'] * num_samples)
        
        # Scale the data and train the classifier
        X_scaled = self.scaler.fit_transform(X)
        self.classifier.fit(X_scaled, y)
        self.is_trained = True
        print("Model training complete.")

    def predict(self, eeg_data):
        """
        Predicts the intent from a single EEG data point.
        Returns 'select' or 'no_action'.
        """
        if not self.is_trained:
            return 'no_action'
        
        # The model expects 2D data, so we reshape our 1D data point
        data_point = eeg_data.reshape(1, -1)
        scaled_data = self.scaler.transform(data_point)
        prediction = self.classifier.predict(scaled_data)[0]
        return prediction

# --- 3. Graphical User Interface (GUI) ---
# This is the on-screen keyboard the user interacts with.
class VirtualKeyboard:
    def __init__(self, model, eeg_simulator):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("BCI Virtual Keyboard Simulator")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.text_font = pygame.font.SysFont('Arial', 32)

        self.model = model
        self.eeg_simulator = eeg_simulator
        
        self.typed_text = ""
        self.current_key = None
        self.selection_timer = 0
        self.selection_delay = 2000 # milliseconds to "focus" on a key

        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/'],
            ['SPACE', '<--'] # Backspace
        ]
        self.key_rects = self._create_key_rects()

    def _create_key_rects(self):
        """Create pygame.Rect objects for each key for drawing and clicking."""
        rects = {}
        key_w, key_h = 60, 50
        spacing = 5
        start_x, start_y = 50, 100
        
        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                if key == 'SPACE':
                    w = key_w * 5 + spacing * 4
                else:
                    w = key_w
                x = start_x + col_idx * (key_w + spacing)
                y = start_y + row_idx * (key_h + spacing)
                rects[key] = pygame.Rect(x, y, w, key_h)
        return rects

    def run(self):
        """The main loop for the keyboard application."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # In a real BCI, you wouldn't use mouse clicks.
                # This is for simulation purposes.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_key_press(event.pos)
            
            # Highlight the key under the mouse cursor (simulating gaze)
            mouse_pos = pygame.mouse.get_pos()
            self.current_key = None
            for key, rect in self.key_rects.items():
                if rect.collidepoint(mouse_pos):
                    self.current_key = key
                    # In a real BCI, this is where you'd continuously stream
                    # EEG data and look for a "selection" signal.
                    # For this sim, we trigger selection on a timer.
                    self._process_bci_selection()
                    break
            
            self._draw()
            self.clock.tick(60)

        pygame.quit()

    def _process_bci_selection(self):
        """Simulate the BCI selection process."""
        now = pygame.time.get_ticks()
        if now - self.selection_timer > self.selection_delay:
            # This is the core BCI logic:
            # 1. Get EEG data
            eeg_data = self.eeg_simulator.get_data()
            
            # 2. Get model prediction
            prediction = self.model.predict(eeg_data)
            
            # 3. If prediction is 'select', perform the action
            if prediction == 'select':
                self._handle_key_press(pygame.mouse.get_pos())
            
            self.selection_timer = now

    def _handle_key_press(self, pos):
        """Handles the action of a key being selected."""
        for key, rect in self.key_rects.items():
            if rect.collidepoint(pos):
                if key == '<--':
                    self.typed_text = self.typed_text[:-1]
                elif key == 'SPACE':
                    self.typed_text += ' '
                else:
                    self.typed_text += key
                break # Only handle one key press at a time

    def _draw(self):
        """Draws all elements on the screen."""
        self.screen.fill((20, 20, 30)) # Dark background

        # Draw typed text at the top
        text_surface = self.text_font.render(self.typed_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (20, 20))

        # Draw the keyboard
        for key, rect in self.key_rects.items():
            color = (70, 70, 90)
            if key == self.current_key:
                # Highlight the currently focused key
                highlight_progress = (pygame.time.get_ticks() - self.selection_timer) / self.selection_delay
                color = (
                    int(70 + (185 * highlight_progress)),
                    int(70 + (50 * highlight_progress)),
                    90
                )
            
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            
            key_text = key.replace('SPACE', 'Space')
            text_surface = self.font.render(key_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

        # Draw instructions
        instructions = [
            "Simulated BCI Virtual Keyboard",
            "Hover over a key to 'focus'. The system will 'type' it automatically.",
            "Press the window's close button to exit."
        ]
        for i, line in enumerate(instructions):
            inst_surface = pygame.font.SysFont('Arial', 16).render(line, True, (180, 180, 180))
            self.screen.blit(inst_surface, (20, self.height - 60 + i * 20))

        pygame.display.flip()

if __name__ == "__main__":
    # Instantiate the components and run the keyboard
    eeg_source = SimulatedEEG()
    bci_brain = BCIModel()
    keyboard_app = VirtualKeyboard(model=bci_brain, eeg_simulator=eeg_source)
    keyboard_app.run()
