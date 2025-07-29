# piece.py
# Define the Piece class for chess pieces

class Piece:
    def __init__(self, row, col, color, ptype):
        self.row = row
        self.col = col
        self.color = color  # 'white' or 'black'
        self.ptype = ptype  # 'K', 'Q', 'R', 'B', 'N', 'P'

    def move(self, row, col):
        self.row = row
        self.col = col

    def copy(self):
        return Piece(self.row, self.col, self.color, self.ptype)

    def __repr__(self):
        return f"Piece({self.color}, {self.ptype}, row={self.row}, col={self.col})"
