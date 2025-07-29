# main.py
# Entry point for the checkers game

from game import Game

def main():
    game = Game()
    print("Chess game started.")
    def print_board_with_coords(board):
        # Print column labels
        print('    a  b  c  d  e  f  g  h')
        for i, row in enumerate(board.board):
            row_str = f'{8 - i} '
            for piece in row:
                if piece is None:
                    row_str += ' . '
                else:
                    symbol = piece.ptype if piece.color == 'white' else piece.ptype.lower()
                    row_str += f' {symbol} '
            print(row_str + f'{8 - i}')
        print('    a  b  c  d  e  f  g  h')

    # Choose game mode
    print("Select game mode:")
    print("1. Play vs Bot")
    print("2. Play vs Human")
    while True:
        mode = input("Enter 1 or 2: ").strip()
        if mode in ['1', '2']:
            break
        print("Invalid input. Please enter 1 or 2.")

    if mode == '1':
        while True:
            color = input("Choose your color (w for White, b for Black): ").strip().lower()
            if color in ['w', 'b']:
                break
            print("Invalid input. Please enter 'w' or 'b'.")
        user_color = 'white' if color == 'w' else 'black'
        while not game.is_game_over():
            print_board_with_coords(game.board)
            if game.current_player == user_color:
                move = input("Enter your move (e.g., e2e4): ")
                if not game.make_move(move):
                    print("Invalid move. Try again.")
            else:
                print(f"AI is thinking... (as {game.current_player})")
                # Show all possible moves for debugging
                all_moves = []
                for piece in game.board.get_all_pieces(game.current_player):
                    from_sq = (piece.row, piece.col)
                    for to_sq in game.get_valid_moves(from_sq):
                        move_str = chr(from_sq[1] + ord('a')) + str(8 - from_sq[0]) + chr(to_sq[1] + ord('a')) + str(8 - to_sq[0])
                        all_moves.append(move_str)
                print(f"AI possible moves: {all_moves}")
                ai_move = game.get_ai_move()
                if ai_move is None:
                    print("AI has no valid moves! Game should be over.")
                    break
                print(f"AI plays: {ai_move}")
                game.make_move(ai_move)
    else:
        while not game.is_game_over():
            print_board_with_coords(game.board)
            move = input(f"{game.current_player.capitalize()} to move (e.g., e2e4): ")
            if not game.make_move(move):
                print("Invalid move. Try again.")
    print(game.board)
    print(f"Game over! Winner: {game.get_winner()}")

if __name__ == "__main__":
    main()
