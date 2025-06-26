
# FNaITMO - Horror Exploration Game

A horror-themed exploration game set in a university environment. Collect papers while navigating through eerie locations and communicate with mysterious chat bots to uncover secrets.

## Features
- Exploration-based gameplay with multiple locations
- Collectible items system
- In-game chat system with different characters
- Collision detection and smooth movement
- Map transitions and camera system

## Requirements
- Python 3.7+
- Pygame: pip install pygame
- Keyboard: pip install keyboard
- Tkinter (usually included with Python)

## How to Run

1. Install dependencies:

   ```bash
   pip install pygame keyboard
   ```

Start the game from the main menu:
```
bash
python main.py
```


**In the main menu:**

Click the "Start" button to launch both:
- The game (game.py)
- The chat system (chat.py)


**Controls**
In-game (game.py)
- WASD: Move character
- Mouse: Click on menu items

Chat System (chat.py)
- Q: Open/close chat window
- Enter: Send message
- Tab: Switch between chat tabs


**Project Structure**
.
├── main.py            # Main menu launcher
├── game.py            # Main game logic
├── chat.py            # Chat system implementation
├── walls.py           # Collision detection system
├── maps/              # Game map images
├── hero/              # Player character sprites
├── textures/          # Game assets (papers, UI elements)
├── icon/              # Menu assets
└── README.md          # This file


**Gameplay**
- Explore different locations (classrooms, hallways, bathrooms)
- Collect all 8 hidden papers
- Use the chat system (press Q) to communicate with:
- Math Teacher (МАТАН-БАЗА)
- Tech Support (Техподдержка)
- Solve the mystery of the university


**Troubleshooting**
If you encounter issues:
- Verify all image files are in correct directories
- Ensure required Python packages are installed
- Check console for error messages