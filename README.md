# README.md

# Chess Game (Pygame)

A modern, interactive chess game built with Python and Pygame. Supports both drag-and-drop and click-to-move, play vs AI (minimax) or another human, and board flipping for black.

## Features
- Play vs Bot (Minimax AI) or Human
- Drag-and-drop and click-to-move support
- Board flips for black player
- Move highlighting, undo, and more
- Modern, clean UI

## Requirements
- Python 3.8+
- pygame

## How to Start the Game
1. Install dependencies:
   ```bash
   pip install pygame
   ```
2. Start the game by running:
   ```bash
   python chess_visual.py
   ```
   This will launch the chess GUI. Use the menu to select your playing mode.

## Project Structure & File Roles
- `chess_visual.py` — Main entry point and GUI. Handles the game window, drawing, user input, and menu.
- `game.py` — Core game logic: move validation, turn management, check/checkmate/stalemate, and game state.
- `ai.py` — Minimax AI for computer opponent. Contains the logic for the bot's move selection.
- `board.py` — Board representation and piece management. Handles the 8x8 grid and piece placement.
- `piece.py` — Piece class and movement rules for each chess piece.
- `constants.py` — Constants for colors, piece types, and other configuration values.
- `assets/` — Images for chess pieces and board graphics.

## License
MIT License

Copyright (c) 2025 [Nitik Sangwan]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
