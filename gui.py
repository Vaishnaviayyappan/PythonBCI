# gui.py
import pygame
import time
from config import *

class VirtualKeyboardGUI:
    def __init__(self, bci_processor):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("EEG Virtual Keyboard (SSVEP)")
        self.clock = pygame.time.Clock()
        
        self.bci_processor = bci_processor
        self.font = pygame.font.SysFont('Arial', 32)
        self.typed_text = ""
        self.last_prediction_time = 0
        self.cooldown_period = 3 # seconds between selections
        
        self.key_rects = self._create_key_rects()

    def _create_key_rects(self):
        rects = {}
        key_w, key_h = 80, 60
        spacing = 10
        start_x, start_y = 50, 150
        
        for i, (key, freq) in enumerate(KEY_FREQUENCIES.items()):
            row = i // 5
            col = i % 5
            x = start_x + col * (key_w + spacing)
            y = start_y + row * (key_h + spacing)
            rects[key] = {'rect': pygame.Rect(x, y, key_w, key_h), 'freq': freq}
        return rects

    def _draw_flickering_key(self, key, key_info):
        """Draw a key that flickers at its designated frequency."""
        rect, freq = key_info['rect'], key_info['freq']
        
        # Calculate if the key should be "on" or "off" based on time
        period = 1.0 / freq
        is_on = (time.time() % period) < (period / 2)
        
        color = (100, 200, 100) if is_on else (50, 50, 50)
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        
        key_text = key if key != '<' else 'BKSP'
        key_text = key_text if key != ' ' else 'SPACE'
        text_surface = self.font.render(key_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Get prediction from BCI processor
            current_time = time.time()
            if current_time - self.last_prediction_time > self.cooldown_period:
                predicted_key, confidence = self.bci_processor.predict()
                
                if predicted_key:
                    print(f"Detected: {predicted_key} with confidence: {confidence:.2f}")
                    if predicted_key == '<':
                        self.typed_text = self.typed_text[:-1]
                    else:
                        self.typed_text += predicted_key
                    self.last_prediction_time = current_time
            
            # --- Drawing ---
            self.screen.fill((20, 20, 30))
            
            # Draw typed text
            text_surface = self.font.render(self.typed_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (50, 50))
            
            # Draw flickering keyboard
            for key, key_info in self.key_rects.items():
                self._draw_flickering_key(key, key_info)
            
            # Draw instructions
            inst_text = pygame.font.SysFont('Arial', 16).render(
                "Look at a flickering key to select it. Closing the window will stop EEG streaming.", 
                True, (180, 180, 180)
            )
            self.screen.blit(inst_text, (50, self.height - 30))
            
            pygame.display.flip()
            clock.tick(60) # Limit framerate to 60 FPS
        
        self.bci_processor.disconnect()
        pygame.quit()
