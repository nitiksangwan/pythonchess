# ai.py
# Upgraded Chess AI using Minimax with Alpha-Beta Pruning and a smarter evaluation function

import math
from copy import deepcopy

class AI:
    # Assign basic piece values for evaluation
    PIECE_VALUES = {
        'K': 1000,  # King is given a very high value to prioritize its safety
        'Q': 9,     # Queen
        'R': 5,     # Rook
        'B': 3,     # Bishop
        'N': 3,     # Knight
        'P': 1      # Pawn
    }

    # Define center squares on the chessboard (d4, e4, d5, e5)
    CENTER_SQUARES = {(3, 3), (3, 4), (4, 3), (4, 4)}

    def __init__(self, depth):
        # Max search depth of minimax algorithm
        self.depth = depth

    # Piece-square tables for positional evaluation
    PAWN_TABLE = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 5, 5, 5, 5, 5, 5, 5],
        [1, 1, 2, 3, 3, 2, 1, 1],
        [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
        [0.5, 1, 1, -2, -2, 1, 1, 0.5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    KNIGHT_TABLE = [
        [-5, -4, -3, -3, -3, -3, -4, -5],
        [-4, -2, 0, 0, 0, 0, -2, -4],
        [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
        [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
        [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
        [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
        [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
        [-5, -4, -3, -3, -3, -3, -4, -5]
    ]

    BISHOP_TABLE = [
        [-2, -1, -1, -1, -1, -1, -1, -2],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
        [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
        [-1, 0, 1, 1, 1, 1, 0, -1],
        [-1, 1, 1, 1, 1, 1, 1, -1],
        [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
        [-2, -1, -1, -1, -1, -1, -1, -2]
    ]

    ROOK_TABLE = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0.5, 1, 1, 1, 1, 1, 1, 0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
        [0, 0, 0, 0.5, 0.5, 0, 0, 0]
    ]

    QUEEN_TABLE = [
        [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
        [-1, 0, 0, 0, 0, 0, 0, -1],
        [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
        [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
        [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
        [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
        [-1, 0, 0.5, 0, 0, 0, 0, -1],
        [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
    ]

    KING_TABLE = [
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-3, -4, -4, -5, -5, -4, -4, -3],
        [-2, -3, -3, -4, -4, -3, -3, -2],
        [-1, -2, -2, -2, -2, -2, -2, -1],
        [2, 2, 0, 0, 0, 0, 2, 2],
        [2, 3, 1, 0, 0, 1, 3, 2]
    ]

    def evaluate(self, board, game, color):
        """
        Evaluate board position from the perspective of `color`.
        Positive score means good for `color`, negative means bad.
        """
        score = 0

        # Get all pieces for both sides
        white_pieces = board.get_all_pieces('white')
        black_pieces = board.get_all_pieces('black')

        # --- MATERIAL COUNT (sum of piece values) ---
        for piece in white_pieces:
            score += self.PIECE_VALUES.get(piece.ptype, 0)
            # Add piece-square table value
            score += self.get_piece_square_value(piece, True)
        for piece in black_pieces:
            score -= self.PIECE_VALUES.get(piece.ptype, 0)
            # Subtract piece-square table value
            score -= self.get_piece_square_value(piece, False)

        # --- CENTER CONTROL BONUS ---
        for piece in white_pieces:
            if (piece.row, piece.col) in self.CENTER_SQUARES:
                score += 0.2  # small bonus for occupying center
        for piece in black_pieces:
            if (piece.row, piece.col) in self.CENTER_SQUARES:
                score -= 0.2

        # --- MOBILITY BONUS (number of legal moves) ---
        # Encourages more flexible positions with more choices
        score += 0.05 * len(self.get_all_moves(board, game, 'white'))
        score -= 0.05 * len(self.get_all_moves(board, game, 'black'))

        # If AI is playing as black, invert score
        return score if color == 'white' else -score

    def get_piece_square_value(self, piece, is_white):
        # Get piece-square table value for a piece
        row = piece.row if is_white else 7 - piece.row
        col = piece.col
        if piece.ptype == 'P':
            return self.PAWN_TABLE[row][col]
        elif piece.ptype == 'N':
            return self.KNIGHT_TABLE[row][col]
        elif piece.ptype == 'B':
            return self.BISHOP_TABLE[row][col]
        elif piece.ptype == 'R':
            return self.ROOK_TABLE[row][col]
        elif piece.ptype == 'Q':
            return self.QUEEN_TABLE[row][col]
        elif piece.ptype == 'K':
            return self.KING_TABLE[row][col]
        return 0

    def minimax(self, board, game, depth, maximizing_player, color, alpha=-math.inf, beta=math.inf):
        """
        Minimax search with alpha-beta pruning.
        Returns a tuple: (evaluation_score, best_move_string)
        """
        if depth == 0 or game.is_game_over():
            return self.evaluate(board, game, color), None

        best_move = None

        if maximizing_player:
            # AI is trying to maximize its score
            max_eval = -math.inf
            for new_board, new_game, move_str in self.get_all_moves(board, game, color):
                # Recursively evaluate the move
                evaluation = self.minimax(new_board, new_game, depth - 1, False, color, alpha, beta)[0]
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move_str
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break  # Prune the remaining branches
            return max_eval, best_move

        else:
            # Opponent is minimizing AI's score
            min_eval = math.inf
            opponent = 'black' if color == 'white' else 'white'
            for new_board, new_game, move_str in self.get_all_moves(board, game, opponent):
                evaluation = self.minimax(new_board, new_game, depth - 1, True, color, alpha, beta)[0]
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move_str
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break  # Prune
            return min_eval, best_move

    def get_all_moves(self, board, game, color):
        """
        Generate all legal moves for a given color.
        Returns list of tuples: (new_board, new_game, move_str)
        """
        import copy
        moves = []

        # Loop through each piece of the current player
        for piece in board.get_all_pieces(color):
            from_sq = (piece.row, piece.col)

            # Get all valid destinations for the piece
            for to_sq in game.get_valid_moves(from_sq):
                # Create deep copies of board and game to avoid state corruption
                new_board = copy.deepcopy(board)
                new_game = copy.deepcopy(game)

                # Make the move on the copied game and board
                new_game._make_move_no_check(from_sq, to_sq)

                # Convert move to algebraic string (e.g., e2e4)
                move_str = (
                    chr(from_sq[1] + ord('a')) + str(8 - from_sq[0]) +
                    chr(to_sq[1] + ord('a')) + str(8 - to_sq[0])
                )

                # Add current board and game state and move string to list
                moves.append((new_board, new_game, move_str))

        return moves
