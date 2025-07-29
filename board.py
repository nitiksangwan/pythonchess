# board.py
# Define the Board class with board state and move generation logic


from constants import ROWS, COLS
from piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    def create_board(self):
        # Set up chess starting position
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        # Place black pieces
        self.board[0] = [
            Piece(0, 0, 'black', 'R'), Piece(0, 1, 'black', 'N'), Piece(0, 2, 'black', 'B'), Piece(0, 3, 'black', 'Q'),
            Piece(0, 4, 'black', 'K'), Piece(0, 5, 'black', 'B'), Piece(0, 6, 'black', 'N'), Piece(0, 7, 'black', 'R')
        ]
        self.board[1] = [Piece(1, col, 'black', 'P') for col in range(COLS)]
        # Place white pieces
        self.board[6] = [Piece(6, col, 'white', 'P') for col in range(COLS)]
        self.board[7] = [
            Piece(7, 0, 'white', 'R'), Piece(7, 1, 'white', 'N'), Piece(7, 2, 'white', 'B'), Piece(7, 3, 'white', 'Q'),
            Piece(7, 4, 'white', 'K'), Piece(7, 5, 'white', 'B'), Piece(7, 6, 'white', 'N'), Piece(7, 7, 'white', 'R')
        ]

    def get_piece(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None

    def move_piece(self, piece, row, col):
        self.board[piece.row][piece.col] = None
        self.board[row][col] = piece
        piece.move(row, col)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == color:
                    pieces.append(piece)
        return pieces

    def __repr__(self):
        board_str = ""
        for row in self.board:
            for piece in row:
                if piece is None:
                    board_str += ". "
                else:
                    symbol = piece.ptype if piece.color == 'white' else piece.ptype.lower()
                    board_str += symbol + " "
            board_str += "\n"
        return board_str
