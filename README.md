# 🦈 Baby Shark Escape

An interactive game designed for infants (around 7 months old) that uses webcam hand tracking to create an engaging play experience. A cute cartoon shark follows the baby's hand movements on screen, helping develop hand-eye coordination and cause-and-effect understanding.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **Real-time Hand Tracking**: Uses Google's MediaPipe for accurate palm detection
- **Smooth Animation**: Shark sprite animates with a swimming tail motion
- **Dynamic Movement**: Shark rotates to face its direction of travel
- **Speed-based Animation**: Faster movement = faster tail wagging
- **Fullscreen Display**: Maximized borderless window for immersive experience
- **High-quality Camera**: Supports up to 1920x1080 resolution

## 🎮 How It Works

1. The game displays your webcam feed as the background
2. Move your hand in front of the camera
3. The shark will follow your hand movements
4. The shark's tail animates faster when it swims faster

## 📋 Requirements

- Python 3.8 - 3.11 (Python 3.12+ may have compatibility issues)
- Webcam
- Windows / macOS / Linux

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/babyshark-game.git
cd babyshark-game
```

### 2. Set up Python environment (recommended: Python 3.10)

```bash
# Using pyenv (recommended)
pyenv install 3.10.11
pyenv local 3.10.11

# Or use your system Python if it's 3.8-3.11
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the game

```bash
python main.py
```

Press **ESC** to exit the game.

## 📁 Project Structure

```
babyshark-game/
├── main.py              # Entry point - game loop
├── requirements.txt     # Python dependencies
├── game/                # Game modules
│   ├── __init__.py      # Package initialization
│   ├── config.py        # Configuration constants
│   ├── camera.py        # Webcam capture and processing
│   ├── hand_tracking.py # MediaPipe hand detection
│   └── shark.py         # Shark entity with AI and animation
└── assets/              # Game assets
    ├── shark-left.png   # Tail left animation frame
    ├── shark-middle.png # Tail center animation frame
    └── shark-right.png  # Tail right animation frame
```

## ⚙️ Configuration

Edit `game/config.py` to customize the game:

### Display Settings
| Variable | Default | Description |
|----------|---------|-------------|
| `DEFAULT_WIDTH` | 1200 | Default window width |
| `DEFAULT_HEIGHT` | 800 | Default window height |
| `GAME_TITLE` | "Baby Shark Escape" | Window title |

### Shark Settings
| Variable | Default | Description |
|----------|---------|-------------|
| `SHARK_SIZE` | 200 | Shark sprite width in pixels |
| `MAX_SPEED` | 10 | Maximum movement speed |
| `ACCEL` | 0.5 | Acceleration rate |
| `DAMPING` | 0.95 | Velocity damping (friction) |

### Hand Tracking
| Variable | Default | Description |
|----------|---------|-------------|
| `MIN_DETECTION_CONFIDENCE` | 0.7 | Hand detection sensitivity |
| `MIN_TRACKING_CONFIDENCE` | 0.5 | Tracking accuracy threshold |

## 🎨 Custom Assets

To use your own shark images:

1. Create 3 PNG images for the tail animation:
   - `shark-left.png` - tail pointing left
   - `shark-middle.png` - tail centered
   - `shark-right.png` - tail pointing right

2. Place them in the `assets/` folder

3. Images should have the shark head pointing UP (12 o'clock position)

## 🔧 Troubleshooting

### "No module named 'cv2'" or MediaPipe errors
```bash
# Use Python 3.10 instead of newer versions
pyenv local 3.10.11
pip install -r requirements.txt
```

### Camera not detected
- Ensure no other application is using the webcam
- Try changing `camera_index=0` to `camera_index=1` in `game/camera.py`

### Low framerate
- Close other applications
- Reduce camera resolution in `game/camera.py`
- Ensure adequate lighting for hand detection

## 🧑‍💻 Development

### Running tests
```bash
python test_imports.py
```

### Adding new features
The modular structure makes it easy to extend:
- Add new entities in `game/`
- Modify AI behavior in `shark.py`
- Adjust physics in `config.py`

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) - Google's hand tracking solution
- [Pygame](https://www.pygame.org/) - Game development library
- [OpenCV](https://opencv.org/) - Camera capture and image processing

## 👨‍👩‍👧 For Parents

**Safety Tips:**
- Limit screen time for infants (AAP recommends minimal screen time for children under 18 months)
- Ensure appropriate screen brightness
- Maintain adequate distance from the screen
- Use this as an interactive bonding activity, not passive entertainment

---

Made with ❤️ for babies everywhere 🦈
