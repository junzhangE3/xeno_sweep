# Alien Minesweeper: Xeno Sweep

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![Pygame Version](https://img.shields.io/badge/pygame-2.x-green.svg)

A fun, pixel-art themed Minesweeper game built with Python and Pygame, featuring an alien twist and an NPC companion! Navigate treacherous alien sectors, locate volatile Xeno Pods, and clear the area with the help of your co-pilot, Zylar.

---

## 🚀 Screenshot

*Replace this with an actual screenshot of your game!*

![Gameplay Screenshot of Alien Minesweeper](path_to_your_screenshot.png)

---

## ✨ Features

- **Classic Minesweeper Gameplay:** With a unique alien theme.
- **Pixel Art Aesthetics:** Retro-inspired visuals and a custom pixel font.
- **Keyboard Controls:**
  - Arrow Keys: Move selection cursor.
  - Enter: Reveal (scan) selected cell.
  - Spacebar: Flag/Unflag selected cell.
  - 'R' Key: Rescan (reset) the game.
- **NPC Companion (Zylar):**
  - Provides dynamic commentary on game events.
  - Displays persistent game instructions.
- **Dynamic UI:**
  - Mine (Pod) counter.
  - Elapsed game timer.
  - Themed buttons and icons.
- **Resizable Window:** Designed for a 16:9 aspect ratio with a larger play area.
- **Clear Game States:** Distinct visual cues for playing, winning, and losing.

---

## 🛠️ Tech Stack & Dependencies

- **Python:** 3.7+
- **Pygame:** 2.x (for graphics, sound, and input)

---

## 🏁 Getting Started

### Prerequisites

- Python 3.7 or higher installed on your system.
- `pip` (Python package installer).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/xeno_sweep.git
   cd xeno_sweep
   ```
2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Alternatively, install Pygame manually:*
   ```bash
   pip install pygame
   ```
4. **Ensure Assets are Present:**
   - Place the pixel font `PressStart2P-Regular.ttf` in the root directory. You can download it from [Google Fonts](https://fonts.google.com/specimen/Press+Start+2P).
   - Place the `alien_head_icon.png` in the root directory.

### Running the Game

Execute the main Python script:
```bash
python xeno_sweep.py
```
(Or `python3 xeno_sweep.py` depending on your system setup)

---

## 🎮 How to Play

- **Objective:** Reveal all cells on the grid that do *not* contain a hidden Xeno-Pod (mine).
- **Numbers:** If you reveal a cell with a number, that number indicates how many Xeno-Pods are hidden in the 8 cells immediately surrounding it.
- **Flags/Beacons:** Use Spacebar to place a beacon on cells you suspect contain a Xeno-Pod. This helps you keep track and prevents accidental reveals.
- **Winning:** Successfully reveal all safe cells.
- **Losing:** Reveal a cell containing a Xeno-Pod.

### Controls

- **Arrow Keys:** Move the selection cursor on the grid.
- **Enter / Return:** Reveal the selected cell.
- **Spacebar:** Place or remove a beacon (flag) on the selected cell.
- **R:** Rescan (reset) the game.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details. 