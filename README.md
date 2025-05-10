# Alien Minesweeper: Xeno Sweep

<!-- ======== Core Badges (Already in your README) ======== -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Pygame Version](https://img.shields.io/badge/pygame-2.x-green.svg)](https://www.pygame.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<!-- ======== GitHub Specific Badges (Some already in your README) ======== -->
[![GitHub stars](https://img.shields.io/github/stars/junzhangE3/xeno_sweep.svg?style=social&label=Star)](https://github.com/junzhangE3/xeno_sweep)
[![GitHub forks](https://img.shields.io/github/forks/junzhangE3/xeno_sweep.svg?style=social&label=Fork)](https://github.com/junzhangE3/xeno_sweep)
[![GitHub issues](https://img.shields.io/github/issues/junzhangE3/xeno_sweep)](https://github.com/junzhangE3/xeno_sweep/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/junzhangE3/xeno_sweep)](https://github.com/junzhangE3/xeno_sweep/pulls)
[![GitHub repo size](https://img.shields.io/github/repo-size/junzhangE3/xeno_sweep)](https://github.com/junzhangE3/xeno_sweep)
[![GitHub last commit](https://img.shields.io/github/last-commit/junzhangE3/xeno_sweep)](https://github.com/junzhangE3/xeno_sweep/commits/main)
[![GitHub contributors](https://img.shields.io/github/contributors/junzhangE3/xeno_sweep)](https://github.com/junzhangE3/xeno_sweep/graphs/contributors)

<!-- ======== Project Status / Maintenance ======== -->
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/junzhangE3/xeno_sweep/graphs/commit-activity)
[![Project Status](https://img.shields.io/badge/status-in%20active%20development-orange.svg)](https://github.com/junzhangE3/xeno_sweep)

A fun, pixel-art themed Minesweeper game built with Python and Pygame, featuring an alien twist and an NPC companion! Navigate treacherous alien sectors, locate volatile Xeno Pods, and clear the area with the help of your co-pilot, Zylar.

---

## 🚀 Screenshot

<img width="1353" alt="image" src="https://github.com/user-attachments/assets/f64aae78-65fd-4429-b517-511b94cb4736" />


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

### 🕹️ Controls

- **Arrow Keys:** Move the selection cursor on the grid.
- **Enter / Return:** Reveal the selected cell.
- **Spacebar:** Place or remove a beacon (flag) on the selected cell.
- **R:** Rescan (reset) the game.

### 💡 Future Enhancements (To-Do)
- Implement actual pixel art sprites for mines and flags.
- Add sound effects for various game actions (reveal, flag, explosion, win, lose).
- Include background music.
- Develop more varied NPC dialogue and reactions.
- Create different difficulty levels (grid size, mine density).
- Implement a proper main menu and settings screen.
- Add a high score system.
- More advanced NPC portrait/animations.

### 🙏 Acknowledgements
- The "Press Start 2P" font by CodeMan38.
- Pygame community for the excellent library.
- You, for playing the demo!

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details. 
