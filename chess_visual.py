# chess_visual.py
# Pygame-based visual chess game entry point


import pygame
import os
from game import Game
from constants import ROWS, COLS, SQUARE_SIZE, LIGHT_BROWN, DARK_BROWN, HIGHLIGHT, UNICODE_PIECES

WIDTH, HEIGHT = COLS * SQUARE_SIZE, ROWS * SQUARE_SIZE


pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')
FONT = pygame.font.SysFont('Arial', 44)

# Load board and piece images if available
PIECE_IMAGES = {}
PIECE_FOLDER = os.path.join('assets', 'pieces')
for color in ['w', 'b']:
    for ptype in ['K', 'Q', 'R', 'B', 'N', 'P']:
        fname = f'{color}{ptype}.png'
        fpath = os.path.join(PIECE_FOLDER, fname)
        if os.path.exists(fpath):
            img = pygame.image.load(fpath)
            img = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
            PIECE_IMAGES[color + ptype] = img

# Optional: load a board background image
BOARD_IMAGE = None
BOARD_IMAGE_PATH = os.path.join('assets', 'board.png')
if os.path.exists(BOARD_IMAGE_PATH):
    BOARD_IMAGE = pygame.image.load(BOARD_IMAGE_PATH)
    BOARD_IMAGE = pygame.transform.smoothscale(BOARD_IMAGE, (WIDTH, HEIGHT))

# --- Draw board and pieces ---
def draw_board(win, board, selected, valid_moves, last_move, drag_piece, drag_pos, flipped=False):
    # Draw squares
    # Prepare a small font for tile coordinates
    coord_font = pygame.font.SysFont('Arial', 16)
    for row in range(ROWS):
        for col in range(COLS):
            draw_row = ROWS - 1 - row if flipped else row
            draw_col = COLS - 1 - col if flipped else col
            color = LIGHT_BROWN if (draw_row + draw_col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # Draw algebraic notation (e.g., e4) in the top-left corner of each tile
            file = chr(ord('a') + draw_col)
            rank = str(8 - draw_row)
            coord_text = file + rank
            text_surf = coord_font.render(coord_text, True, (80, 80, 80))
            win.blit(text_surf, (col*SQUARE_SIZE + 4, row*SQUARE_SIZE + 2))
    # Draw board image if available
    if BOARD_IMAGE:
        win.blit(BOARD_IMAGE, (0, 0))
    # Highlight last move
    if last_move:
        for sq in last_move:
            r, c = sq
            if flipped:
                r, c = ROWS - 1 - r, COLS - 1 - c
            pygame.draw.rect(win, HIGHLIGHT, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 6)
    # Highlight selected and valid moves
    if selected:
        r, c = selected
        if flipped:
            r, c = ROWS - 1 - r, COLS - 1 - c
        pygame.draw.rect(win, (255, 255, 0), (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
        for move in valid_moves:
            mr, mc = move
            if flipped:
                mr, mc = ROWS - 1 - mr, COLS - 1 - mc
            pygame.draw.circle(win, (0, 255, 0), (mc*SQUARE_SIZE+SQUARE_SIZE//2, mr*SQUARE_SIZE+SQUARE_SIZE//2), 12)
    # Draw pieces
    for row in range(ROWS):
        for col in range(COLS):
            draw_row = ROWS - 1 - row if flipped else row
            draw_col = COLS - 1 - col if flipped else col
            piece = board.get_piece(draw_row, draw_col)
            if piece:
                if drag_piece:
                    dr, dc = drag_piece
                    if flipped:
                        dr, dc = ROWS - 1 - dr, COLS - 1 - dc
                    if (row, col) == (dr, dc):
                        continue
                key = piece.color[0] + piece.ptype
                if key in PIECE_IMAGES:
                    win.blit(PIECE_IMAGES[key], (col*SQUARE_SIZE, row*SQUARE_SIZE))
                else:
                    text = FONT.render(UNICODE_PIECES[key], True, (0,0,0))
                    win.blit(text, (col*SQUARE_SIZE+8, row*SQUARE_SIZE+8))
    # Draw dragged piece
    if drag_piece and drag_pos:
        dr, dc = drag_piece
        if flipped:
            dr, dc = ROWS - 1 - dr, COLS - 1 - dc
        piece = board.get_piece(dr, dc)
        if piece:
            key = piece.color[0] + piece.ptype
            if key in PIECE_IMAGES:
                win.blit(PIECE_IMAGES[key], (drag_pos[0]-SQUARE_SIZE//2, drag_pos[1]-SQUARE_SIZE//2))
            else:
                text = FONT.render(UNICODE_PIECES[key], True, (0,0,0))
                win.blit(text, (drag_pos[0]-SQUARE_SIZE//2+8, drag_pos[1]-SQUARE_SIZE//2+8))
    pygame.display.update()

def main():


    import copy
    # --- Graphical menu for mode and color selection ---
    # Try to use Bebas Neue or fallback to Arial if not available
    try:
        menu_font = pygame.font.SysFont('Bebas Neue', 40, bold=True)
        small_font = pygame.font.SysFont('Bebas Neue', 24)
    except:
        menu_font = pygame.font.SysFont('Arial', 40, bold=True)
        small_font = pygame.font.SysFont('Arial', 24)
    mode = None
    user_color = 'white'
    selecting = True
    color_select = False
    flipped = False
    while selecting:
        WIN.fill((220, 200, 170))
        # Draw title (no shadow, just simple text)
        title = menu_font.render('CHESS', True, (60, 40, 20))
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 60))

        # Move options back to previous lower positions
        mx, my = pygame.mouse.get_pos()
        mode1_label = menu_font.render('PLAY VS BOT', True, (30, 30, 30))
        mode2_label = menu_font.render('PLAY VS HUMAN', True, (30, 30, 30))
        mode_y1 = 170
        mode_y2 = 250
        mode1_rect = pygame.Rect(0, mode_y1, WIDTH, mode1_label.get_height())
        mode2_rect = pygame.Rect(0, mode_y2, WIDTH, mode2_label.get_height())
        mode1_selected = False
        mode2_selected = False
        if not color_select:
            if mode == '1':
                mode1_selected = True
            elif mode == '2':
                mode2_selected = True
        WIN.blit(mode1_label, (WIDTH//2 - mode1_label.get_width()//2, mode_y1))
        WIN.blit(mode2_label, (WIDTH//2 - mode2_label.get_width()//2, mode_y2))
        if mode1_selected:
            pygame.draw.line(WIN, (30,30,30), (WIDTH//2 - mode1_label.get_width()//2, mode_y1+mode1_label.get_height()+4), (WIDTH//2 + mode1_label.get_width()//2, mode_y1+mode1_label.get_height()+4), 3)
        if mode2_selected:
            pygame.draw.line(WIN, (30,30,30), (WIDTH//2 - mode2_label.get_width()//2, mode_y2+mode2_label.get_height()+4), (WIDTH//2 + mode2_label.get_width()//2, mode_y2+mode2_label.get_height()+4), 3)

        # Color selection
        white_selected = False
        black_selected = False
        if color_select:
            color_msg = small_font.render('CHOOSE YOUR COLOR:', True, (0,0,0))
            WIN.blit(color_msg, (WIDTH//2 - color_msg.get_width()//2, 340))
            white_label = menu_font.render('WHITE', True, (60,60,60))
            black_label = menu_font.render('BLACK', True, (0,0,0))
            color_btn_y = 395
            white_rect = pygame.Rect(WIDTH//2-120, color_btn_y, 100, 50)
            black_rect = pygame.Rect(WIDTH//2+20, color_btn_y, 100, 50)
            if user_color == 'white':
                white_selected = True
            elif user_color == 'black':
                black_selected = True
            WIN.blit(white_label, (WIDTH//2-120+10, color_btn_y))
            WIN.blit(black_label, (WIDTH//2+20+10, color_btn_y))
            # Underline selected color
            if white_selected:
                pygame.draw.line(WIN, (60,60,60), (WIDTH//2-120+10, color_btn_y+white_label.get_height()+4), (WIDTH//2-120+10+white_label.get_width(), color_btn_y+white_label.get_height()+4), 3)
            if black_selected:
                pygame.draw.line(WIN, (0,0,0), (WIDTH//2+20+10, color_btn_y+black_label.get_height()+4), (WIDTH//2+20+10+black_label.get_width(), color_btn_y+black_label.get_height()+4), 3)


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if not color_select:
                    # Check if clicked on mode1 text
                    if mode1_rect.collidepoint(mx, my):
                        mode = '1'
                        color_select = True
                    elif mode2_rect.collidepoint(mx, my):
                        mode = '2'
                        selecting = False
                else:
                    if white_rect.collidepoint(mx, my):
                        user_color = 'white'
                        flipped = False
                        selecting = False
                    elif black_rect.collidepoint(mx, my):
                        user_color = 'black'
                        flipped = True
                        selecting = False

    run = True
    clock = pygame.time.Clock()
    game = Game(visual=True)
    selected = None
    valid_moves = []
    game_over = False
    last_move = None
    dragging = False
    drag_piece = None
    history = []  # Stack of previous game states

    dragging = False
    drag_piece = None
    drag_pos = None
    mouse_moved = False

    while run:
        clock.tick(60)
        if mode == '1' and game.current_player != user_color and not game_over:
            print(f"AI is thinking... (as {game.current_player})")
            ai_move = game.get_ai_move()
            if ai_move is not None:
                history.append(copy.deepcopy(game))
                # ai_move can be either a move string or a tuple ((from_row, from_col), (to_row, to_col))
                # Try to extract the move squares for highlighting
                move_squares = None
                if isinstance(ai_move, tuple) and len(ai_move) == 2 and all(isinstance(x, tuple) and len(x) == 2 for x in ai_move):
                    move_squares = [ai_move[0], ai_move[1]]
                # If ai_move is a string, try to parse it (e.g., 'e2e4')
                elif isinstance(ai_move, str) and len(ai_move) == 4:
                    from_col = ord(ai_move[0]) - ord('a')
                    from_row = 8 - int(ai_move[1])
                    to_col = ord(ai_move[2]) - ord('a')
                    to_row = 8 - int(ai_move[3])
                    move_squares = [(from_row, from_col), (to_row, to_col)]
                game.make_move(ai_move)
                last_move = move_squares
            else:
                print("AI has no valid moves!")
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    # Map input to logical board if flipped
                    logic_row, logic_col = (ROWS - 1 - row, COLS - 1 - col) if flipped else (row, col)
                    mouse_moved = False

                    # If clicking a highlighted move, move there
                    if selected and (logic_row, logic_col) in valid_moves:
                        history.append(copy.deepcopy(game))
                        game.make_move(selected, (logic_row, logic_col))
                        last_move = [selected, (logic_row, logic_col)]
                        selected = None
                        valid_moves = []
                        dragging = False
                        drag_piece = None
                        drag_pos = None
                        continue
                    # If clicking the selected piece again, deselect
                    if selected and (logic_row, logic_col) == selected:
                        selected = None
                        valid_moves = []
                        dragging = False
                        drag_piece = None
                        drag_pos = None
                        continue
                    # If clicking a piece, select and show moves
                    piece = game.board.get_piece(logic_row, logic_col)
                    if piece and piece.color == game.current_player:
                        if mode == '1' and game.current_player != user_color:
                            continue
                        selected = (logic_row, logic_col)
                        valid_moves = game.get_valid_moves(selected)
                        # Enable drag-and-drop
                        dragging = True
                        drag_piece = (logic_row, logic_col)
                        drag_pos = (x, y)
                    else:
                        selected = None
                        valid_moves = []
                        dragging = False
                        drag_piece = None
                        drag_pos = None
                elif event.type == pygame.MOUSEMOTION and dragging:
                    drag_pos = pygame.mouse.get_pos()
                    mouse_moved = True
                elif event.type == pygame.MOUSEBUTTONUP and dragging:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    logic_row, logic_col = (ROWS - 1 - row, COLS - 1 - col) if flipped else (row, col)
                    # If mouse was moved (a drag), and it's a valid move, make the move.
                    if mouse_moved and selected and (logic_row, logic_col) in valid_moves:
                        history.append(copy.deepcopy(game))
                        game.make_move(selected, (logic_row, logic_col))
                        last_move = [selected, (logic_row, logic_col)]
                        selected = None
                        valid_moves = []
                    else:
                        if selected and (logic_row, logic_col) == selected:
                            # Already selected, deselect
                            selected = None
                            valid_moves = []
                        else:
                            piece = game.board.get_piece(logic_row, logic_col)
                            if piece and piece.color == game.current_player:
                                selected = (logic_row, logic_col)
                                valid_moves = game.get_valid_moves(selected)
                            else:
                                selected = None
                                valid_moves = []
                    dragging = False
                    drag_piece = None
                    drag_pos = None
            if event.type == pygame.KEYDOWN:
                # Undo with Ctrl+Z
                if event.key == pygame.K_z and (event.mod & pygame.KMOD_CTRL):
                    if history:
                        game = history.pop()
                        # If vs bot and after undo it's still not user's turn, undo again
                        if mode == '1' and game.current_player != user_color and history:
                            game = history.pop()
                        selected = None
                        valid_moves = []
                        dragging = False
                        drag_piece = None
                        drag_pos = None
                        game_over = False
                        last_move = None
                if game_over:
                    if event.key == pygame.K_r:
                        game = Game(visual=True)
                        selected = None
                        valid_moves = []
                        game_over = False
                        last_move = None
                        history = []
                    elif event.key == pygame.K_q:
                        run = False

        draw_board(WIN, game.board, selected, valid_moves, last_move, drag_piece, drag_pos, flipped)
        if game.is_game_over():
            game_over = True

    pygame.quit()
    # Entry point

if __name__ == "__main__":
    main()
