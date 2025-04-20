import mss
import numpy as np
import cv2
import time
import threading
import pygame
from pynput.keyboard import Key, Controller, Listener

# Initialize pygame and keyboard
pygame.mixer.init()
keyboard = Controller()

# Constants
CARD_PICK_REGION = {"top": 1327, "left": 1580, "width": 42, "height": 42}
FRAME_INTERVAL = 0.1
CARD_TEMPLATES = {
    "gold_card": "gold_card.png",
    "blue_card": "blue_card.webp",
    "red_card": "red_card.png"
}

# Global variables
selecting_card = False
active = True
detection_lock = threading.Lock()

# Preload templates
card_templates = {name: cv2.imread(path, 0) for name, path in CARD_TEMPLATES.items()}

# Preload sounds
SOUND_MAP = {
    "gold_card": "dog.mp3",
    "blue_card": "blue_sound.mp3",
    "red_card": "red_sound.mp3"
}
preloaded_sounds = {}
for card_name, sound_path in SOUND_MAP.items():
    try:
        preloaded_sounds[card_name] = pygame.mixer.Sound(sound_path)
    except Exception as e:
        raise FileNotFoundError(f"Error loading sound {sound_path} for {card_name}: {e}")

def play_card_sound(card_name):
    if card_name in preloaded_sounds:
        try:
            sound = preloaded_sounds[card_name]
            sound.play()
        except Exception as e:
            print(f"Error playing sound for {card_name}: {e}")

def on_press(key):
    global selecting_card, active
    try:
        with detection_lock:
            if getattr(key, 'char', None) == 'e':
                keyboard.press('1')
                keyboard.release('1')
                selecting_card = "gold_card"
                print("Gold card selection mode activated")
            elif getattr(key, 'char', None) == 'w':  # Check for char attribute
                keyboard.press('1')
                keyboard.release('1')
                selecting_card = "blue_card"
                print("Blue card selection mode activated")
            elif getattr(key, 'char', None) == 's':  # Check for char attribute
                keyboard.press('1')
                keyboard.release('1')
                selecting_card = "red_card"
                print("Red card selection mode activated")
            elif key == Key.home:
                active = not active
                print(f"Tool is now {'active' if active else 'inactive'}.")
    except Exception as e:
        print(f"Error handling key press: {e}")

def detect_card():
    global selecting_card, active
    with mss.mss() as sct:
        print("Screen capturing started...")
        last_time = time.time()
        while True:
            current_time = time.time()
            if current_time - last_time < FRAME_INTERVAL:
                time.sleep(0.01)
                continue

            last_time = current_time

            if not active:
                time.sleep(0.1)
                continue

            screenshot = sct.grab(CARD_PICK_REGION)
            image_np = np.array(screenshot)[:, :, :3]

            gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
            detected_card = None
            max_val = 0

            for card_name, template in card_templates.items():
                result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
                _, max_score, _, _ = cv2.minMaxLoc(result)

                if max_score > max_val:
                    max_val = max_score
                    detected_card = card_name

            with detection_lock:
                if selecting_card and detected_card == selecting_card:
                    if max_val >= 0.3:  # Adjust threshold as needed
                        keyboard.press('1')
                        keyboard.release('1')
                        play_card_sound(detected_card)
                        selecting_card = False

if __name__ == "__main__":
    print("Starting Twisted Fate Card Picker Tool...")

    listener = Listener(on_press=on_press)
    listener.start()

    detection_thread = threading.Thread(target=detect_card, daemon=True)
    detection_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        listener.stop()
        pygame.mixer.quit()
