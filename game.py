# game.py
# Implement the game loop and game logic for chess

from board import Board
from ai import AI

class Game:
    def __init__(self, visual=False):
        self.board = Board()
        self.current_player = 'white'
        self.visual = visual
        self.ai = AI(depth=3)
        self.en_passant = None  # (row, col) where en passant is possible
        self.castling_rights = {
            'white': {'K': True, 'Q': True},
            'black': {'K': True, 'Q': True}
        }
        self._history = []  # Stack to store previous states for undo

    def save_state(self):
        # Save current state for undo
        state = {
            'board': [[piece if piece is None else piece.copy() for piece in row] for row in self.board.board],
            'current_player': self.current_player,
            'en_passant': self.en_passant,
            'castling_rights': {
                'white': self.castling_rights['white'].copy(),
                'black': self.castling_rights['black'].copy()
            }
        }
        self._history.append(state)

    def restore_state(self, state):
        # Restore saved state
        self.board.board = [[piece if piece is None else piece.copy() for piece in row] for row in state['board']]
        self.current_player = state['current_player']
        self.en_passant = state['en_passant']
        self.castling_rights = {
            'white': state['castling_rights']['white'].copy(),
            'black': state['castling_rights']['black'].copy()
        }

    def undo_move(self):
        if not self._history:
            return False
        state = self._history.pop()
        self.restore_state(state)
        return True

    def is_game_over(self):
        # Game over if checkmate or stalemate
        if self.get_winner() in ['white', 'black', 'draw']:
            return True
        return False

    def get_winner(self):
        # Returns 'white', 'black', 'draw', or None
        if not self.is_king_alive('white'):
            return 'black'
        if not self.is_king_alive('black'):
            return 'white'
        if self.is_checkmate('white'):
            return 'black'
        if self.is_checkmate('black'):
            return 'white'
        if self.is_stalemate('white') or self.is_stalemate('black'):
            return 'draw'
        return None

    def is_king_alive(self, color):
        for piece in self.board.get_all_pieces(color):
            if piece.ptype == 'K':
                return True
        return False

    def is_in_check(self, color):
        # Find king position
        king_pos = None
        for piece in self.board.get_all_pieces(color):
            if piece.ptype == 'K':
                king_pos = (piece.row, piece.col)
                break
        if not king_pos:
            return False
        # Check if any enemy piece attacks king
        enemy = 'black' if color == 'white' else 'white'
        for piece in self.board.get_all_pieces(enemy):
            for move in self.get_pseudo_legal_moves((piece.row, piece.col)):
                if move == king_pos:
                    return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        for piece in self.board.get_all_pieces(color):
            for move in self.get_legal_moves((piece.row, piece.col)):
                return False
        return True

    def is_stalemate(self, color):
        if self.is_in_check(color):
            return False
        for piece in self.board.get_all_pieces(color):
            if self.get_legal_moves((piece.row, piece.col)):
                return False
        return True

    def make_move(self, move_from, move_to=None):
        # move_from: (row, col) or string like 'e2e4'
        # move_to: (row, col) or None
        if isinstance(move_from, str):
            # Parse move like 'e2e4'
            if len(move_from) == 4:
                from_sq = (8 - int(move_from[1]), ord(move_from[0]) - ord('a'))
                to_sq = (8 - int(move_from[3]), ord(move_from[2]) - ord('a'))
            else:
                return False
        else:
            from_sq = move_from
            to_sq = move_to
        piece = self.board.get_piece(*from_sq)
        if not piece or piece.color != self.current_player:
            return False
        valid_moves = self.get_legal_moves(from_sq)
        if to_sq not in valid_moves:
            return False

        # En passant
        if piece.ptype == 'P' and self.en_passant and to_sq == self.en_passant:
            direction = -1 if piece.color == 'white' else 1
            self.board.board[to_sq[0] + (1 if piece.color == 'white' else -1)][to_sq[1]] = None

        # Castling
        if piece.ptype == 'K' and abs(to_sq[1] - from_sq[1]) == 2:
            # King-side
            if to_sq[1] == 6:
                rook = self.board.get_piece(from_sq[0], 7)
                self.board.move_piece(rook, from_sq[0], 5)
            # Queen-side
            elif to_sq[1] == 2:
                rook = self.board.get_piece(from_sq[0], 0)
                self.board.move_piece(rook, from_sq[0], 3)

        # Move the piece
        self.board.move_piece(piece, *to_sq)

        # Pawn promotion (to queen only)
        if piece.ptype == 'P' and (to_sq[0] == 0 or to_sq[0] == 7):
            piece.ptype = 'Q'

        # Update en passant
        if piece.ptype == 'P' and abs(to_sq[0] - from_sq[0]) == 2:
            self.en_passant = ((from_sq[0] + to_sq[0]) // 2, from_sq[1])
        else:
            self.en_passant = None

        # Update castling rights
        if piece.ptype == 'K':
            self.castling_rights[piece.color]['K'] = False
            self.castling_rights[piece.color]['Q'] = False
        if piece.ptype == 'R':
            if from_sq[1] == 0:
                self.castling_rights[piece.color]['Q'] = False
            elif from_sq[1] == 7:
                self.castling_rights[piece.color]['K'] = False

        # Log the move with player color using board locations like a2, a4
        def to_board_loc(pos):
            return chr(pos[1] + ord('a')) + str(8 - pos[0])
        print(f"{self.current_player.capitalize()} moved: {to_board_loc(from_sq)} to {to_board_loc(to_sq)}")

        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True

    def get_valid_moves(self, pos):
        # Returns only legal moves (not leaving king in check)
        return self.get_legal_moves(pos)

    def get_legal_moves(self, pos):
        # Returns a list of legal (row, col) destinations for the piece at pos
        # If pos is a color string, return all legal moves for that color
        if isinstance(pos, str) and pos in ('white', 'black'):
            moves = []
            for piece in self.board.get_all_pieces(pos):
                from_sq = (piece.row, piece.col)
                for to_sq in self.get_legal_moves(from_sq):
                    moves.append((from_sq, to_sq))
            return moves
        # If pos is algebraic notation (e.g., 'e2'), convert to (row, col)
        if isinstance(pos, str) and len(pos) == 2 and pos[0].isalpha() and pos[1].isdigit():
            col = ord(pos[0].lower()) - ord('a')
            row = 8 - int(pos[1])
            piece = self.board.get_piece(row, col)
        else:
            piece = self.board.get_piece(int(pos[0]), int(pos[1]))
        if not piece:
            return []
        moves = []
        for move in self.get_pseudo_legal_moves(pos):
            # Make the move on a copy and check if king is in check
            import copy
            game_copy = copy.deepcopy(self)
            game_copy._make_move_no_check(pos, move)
            if not game_copy.is_in_check(piece.color):
                moves.append(move)
        return moves

    def get_pseudo_legal_moves(self, pos):
        # Like get_valid_moves, but does not check for king safety
        piece = self.board.get_piece(*pos)
        if not piece:
            return []
        moves = []
        row, col = pos
        directions = []
        if piece.ptype == 'P':
            direction = -1 if piece.color == 'white' else 1
            # Forward move
            if 0 <= row + direction < 8 and self.board.get_piece(row + direction, col) is None:
                moves.append((row + direction, col))
                # Double move from starting position
                start_row = 6 if piece.color == 'white' else 1
                if row == start_row and self.board.get_piece(row + 2 * direction, col) is None:
                    moves.append((row + 2 * direction, col))
            # Capture
            for dc in [-1, 1]:
                r, c = row + direction, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = self.board.get_piece(r, c)
                    if target and target.color != piece.color:
                        moves.append((r, c))
            # En passant
            if self.en_passant:
                if abs(self.en_passant[1] - col) == 1 and self.en_passant[0] == row + direction:
                    moves.append(self.en_passant)
        elif piece.ptype == 'N':
            for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = self.board.get_piece(r, c)
                    if target is None or target.color != piece.color:
                        moves.append((r, c))
        elif piece.ptype == 'B':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece.ptype == 'R':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        elif piece.ptype == 'Q':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        elif piece.ptype == 'K':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < 8 and 0 <= c < 8:
                        target = self.board.get_piece(r, c)
                        if target is None or target.color != piece.color:
                            moves.append((r, c))
            # Castling
            if self.castling_rights[piece.color]['K']:
                if all(self.board.get_piece(row, c) is None for c in [5, 6]):
                    rook = self.board.get_piece(row, 7)
                    if rook and rook.ptype == 'R' and rook.color == piece.color:
                        moves.append((row, 6))
            if self.castling_rights[piece.color]['Q']:
                if all(self.board.get_piece(row, c) is None for c in [1, 2, 3]):
                    rook = self.board.get_piece(row, 0)
                    if rook and rook.ptype == 'R' and rook.color == piece.color:
                        moves.append((row, 2))
        # Sliding pieces (B, R, Q)
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = self.board.get_piece(r, c)
                if target is None:
                    moves.append((r, c))
                elif target.color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

    def _make_move_no_check(self, move_from, move_to):
        # Like make_move, but does not check for legality (used for move simulation)
        piece = self.board.get_piece(*move_from)
        if not piece:
            return False
        # En passant
        if piece.ptype == 'P' and self.en_passant and move_to == self.en_passant:
            direction = -1 if piece.color == 'white' else 1
            self.board.board[move_to[0] + (1 if piece.color == 'white' else -1)][move_to[1]] = None
        # Castling
        if piece.ptype == 'K' and abs(move_to[1] - move_from[1]) == 2:
            if move_to[1] == 6:
                rook = self.board.get_piece(move_from[0], 7)
                self.board.move_piece(rook, move_from[0], 5)
            elif move_to[1] == 2:
                rook = self.board.get_piece(move_from[0], 0)
                self.board.move_piece(rook, move_from[0], 3)
        self.board.move_piece(piece, *move_to)
        # Pawn promotion (to queen only)
        if piece.ptype == 'P' and (move_to[0] == 0 or move_to[0] == 7):
            piece.ptype = 'Q'
        # Update en passant
        if piece.ptype == 'P' and abs(move_to[0] - move_from[0]) == 2:
            self.en_passant = ((move_from[0] + move_to[0]) // 2, move_from[1])
        else:
            self.en_passant = None
        # Update castling rights
        if piece.ptype == 'K':
            self.castling_rights[piece.color]['K'] = False
            self.castling_rights[piece.color]['Q'] = False
        if piece.ptype == 'R':
            if move_from[1] == 0:
                self.castling_rights[piece.color]['Q'] = False
            elif move_from[1] == 7:
                self.castling_rights[piece.color]['K'] = False
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True

    def get_ai_move(self):
        # Use minimax to get best move for current player
        _, move_str = self.ai.minimax(self.board, self, self.ai.depth, True, self.current_player)
        return move_str
