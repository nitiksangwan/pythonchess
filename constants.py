# constants.py
# Define colors and board dimensions for the chess game

# Colors (RGB tuples)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)

# Board dimensions
ROWS, COLS = 8, 8
SQUARE_SIZE = 80  # size of each square in pixels

# Piece types
PIECE_TYPES = ['K', 'Q', 'R', 'B', 'N', 'P']

# Piece unicode symbols for display (optional for text mode)
UNICODE_PIECES = {
    'wK': '\u2654', 'wQ': '\u2655', 'wR': '\u2656', 'wB': '\u2657', 'wN': '\u2658', 'wP': '\u2659',
    'bK': '\u265A', 'bQ': '\u265B', 'bR': '\u265C', 'bB': '\u265D', 'bN': '\u265E', 'bP': '\u265F',
}
