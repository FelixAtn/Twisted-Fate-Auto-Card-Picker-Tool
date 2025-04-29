
# Twisted Fate Auto Card Picker Tool

A Python-based automation tool that helps **Twisted Fate** players in *League of Legends* automatically pick the correct card (Gold, Blue, or Red) based on keyboard input and screen detection. It utilizes **screen capturing**, **template matching**, and **sound notifications** to enhance your reaction time and gameplay.

## Watch the Video

[Watch the Video](https://www.youtube.com/watch?v=aO-cGoCjDXg)

## Features

- Real-time screen capture and card detection using `mss`, `OpenCV`, and `numpy`
- Keybinds to initiate specific card selection:
  - `E` for Gold card
  - `W` for Blue card
  - `S` for Red card
- Plays a sound when the correct card is successfully detected
- Low-latency image matching with customizable thresholds
- Multithreaded detection loop with a dedicated keyboard listener
- Toggle active/inactive state using the `Home` key

---

### Prerequisites

Make sure you have Python 3.8+ installed and install the required libraries:

```bash
pip install mss numpy opencv-python pygame pynput
```

### File Structure

Place the following image and audio files in the **same directory** as the script:

#### Templates:
- `gold_card.png`
- `blue_card.webp`
- `red_card.png`

#### Sounds:
- `dog.mp3` (Gold card sound)
- `blue_sound.mp3` (Blue card sound)
- `red_sound.mp3` (Red card sound)

> Note: You can customize these image and sound files to your own preference.

---

## How It Works

1. **Start the script**:
   ```bash
   python twisted_fate_picker.py
   ```

2. **Press a key to activate a card selection mode**:
   - `E`: Activates Gold card selection
   - `W`: Activates Blue card selection
   - `S`: Activates Red card selection

3. The tool will:
   - Continuously scan a predefined region of your screen.
   - Match against preloaded templates.
   - Automatically press `1` to lock the card when a match is found.
   - Play a confirmation sound.
   
4. **Toggle detection** on/off at any time by pressing the `Home` key.

---

## How to Customize

### Adjust the Detection Region

Modify `CARD_PICK_REGION` at the top of the script to match your resolution and card pick location:

```python
CARD_PICK_REGION = {"top": 1327, "left": 1580, "width": 42, "height": 42}
```

### Adjust Detection Threshold

To change how sensitive the card match must be:

```python
if max_val >= 0.3:  # Lower = more sensitive
```

---

## Limitations

- The tool assumes a static UI layout (specific resolution and card location).
- Requires accurate template images for best results.
- Not a Riot-approved tool — use at your own discretion in online matches.

---

## Credits

Developed by Felix Atn for educational purposes.
---

## License

This project is licensed under the MIT License.
