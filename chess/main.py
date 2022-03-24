import chess_engine
import ai
import pygame as p
import sys


WIDTH = 712
HIGHT = 522
WIDTH_TABLE = 512
HEIGHT_TABLE = 512
DIMENSION = 8
SQUARE_SIZE = WIDTH_TABLE // DIMENSION
MAX_FPS = 15
IMAGES = {}


# load peace images
def load_images():
    piaces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bp",
              "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "wp"]
    for piace in piaces:
        IMAGES[piace] = p.transform.scale(p.image.load(
            "chess/images/" + piace + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def draw_board(screen):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if (i + j) % 2 == 1:
                p.draw.rect(screen, (107, 156, 79), (i * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2),
                            j * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2), SQUARE_SIZE, SQUARE_SIZE))
            else:
                p.draw.rect(screen, (239, 240, 209), (i * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2),
                            j * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2), SQUARE_SIZE, SQUARE_SIZE))


def draw_piaces(screen, gs):
    for i, row in enumerate(gs.board):
        for j, piace in enumerate(row):
            if piace != "--":
                screen.blit(IMAGES[piace], (j * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2),
                            i * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2), SQUARE_SIZE, SQUARE_SIZE))


def draw_description(screen):
    columns = ("a", "b", "c", "d", "e", "f", "g", "h")
    description = p.font.Font(None, int(SQUARE_SIZE * 0.25))
    for i in range(DIMENSION):
        white_description = description.render(
            str(DIMENSION - i), False, (239, 240, 209))
        green_description = description.render(
            str(DIMENSION - i), False, (107, 156, 79))
        if i % 2 == 1:
            screen.blit(white_description, (HIGHT - HEIGHT_TABLE,
                        i * SQUARE_SIZE + (HIGHT - HEIGHT_TABLE)))
        else:
            screen.blit(green_description, (HIGHT - HEIGHT_TABLE,
                        i * SQUARE_SIZE + (HIGHT - HEIGHT_TABLE)))
    for j in range(DIMENSION):
        white_description = description.render(
            columns[j], False, (239, 240, 209))
        green_description = description.render(
            columns[j], False, (107, 156, 79))
        if j % 2 == 0:
            screen.blit(white_description, (j * SQUARE_SIZE + (HIGHT - HEIGHT_TABLE) + SQUARE_SIZE *
                        0.75, (DIMENSION - 1) * SQUARE_SIZE + (HIGHT - HEIGHT_TABLE) + SQUARE_SIZE * 0.7))
        else:
            screen.blit(green_description, (j * SQUARE_SIZE + (HIGHT - HEIGHT_TABLE) + SQUARE_SIZE *
                        0.75, (DIMENSION - 1) * SQUARE_SIZE + (HIGHT - HEIGHT_TABLE) + SQUARE_SIZE * 0.7))


def end_game(screen, gs):
    end = p.font.Font(None, int(SQUARE_SIZE * 0.7))
    if gs.checkmate:
        end_text = end.render("checkmate", True, "blue")
        screen.blit(end_text, (DIMENSION * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2) +
                    int(SQUARE_SIZE * 0.24), SQUARE_SIZE // 2 - (HIGHT - HEIGHT_TABLE) // 2))
    elif gs.stalemate:
        end_text = end.render("stalemate", True, "blue")
        screen.blit(end_text, (DIMENSION * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2) +
                    int(SQUARE_SIZE * 0.24), SQUARE_SIZE // 2 - (HIGHT - HEIGHT_TABLE) // 2))


def highlight(screen, gs, valid_moves, square_selected):
    if square_selected:
        # highlight square_selected
        r, c = square_selected
        if gs.board[r][c][0] == ("w" if gs.white_to_move else "b"):
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("yellow"))
            screen.blit(s, (c * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2),
                        r * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2)))
            s.fill((0, 0, 0, 255))
            s.set_alpha(150)
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    if gs.board[move.end_row][move.end_col] == "--":
                        if (move.end_col + move.end_row) % 2 == 1:
                            p.draw.circle(screen, (96, 141, 70), (move.end_col * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2) + SQUARE_SIZE //
                                          2, move.end_row * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2) + SQUARE_SIZE // 2), SQUARE_SIZE * 0.2)
                        else:
                            p.draw.circle(screen, (214, 217, 188), (move.end_col * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2) + SQUARE_SIZE //
                                          2, move.end_row * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2) + SQUARE_SIZE // 2), SQUARE_SIZE * 0.2)
                    else:
                        if (move.end_col + move.end_row) % 2 == 1:
                            p.draw.circle(screen, (96, 141, 70), (move.end_col * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2) + SQUARE_SIZE //
                                          2, move.end_row * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2) + SQUARE_SIZE // 2), SQUARE_SIZE * 0.5, 5)
                        else:
                            p.draw.circle(screen, (214, 217, 188), (move.end_col * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2) + SQUARE_SIZE //
                                          2, move.end_row * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2) + SQUARE_SIZE // 2), SQUARE_SIZE * 0.5, 5)


def draw_log(screen, gs):
    size = int(SQUARE_SIZE * 0.35)
    log = p.font.Font(None, size)
    j = len(gs.chess_log) // 43
    if gs.checkmate:
        gs.chess_log[-1] = gs.chess_log[-1] + "#"
    elif gs.check:
        gs.chess_log[-1] = gs.chess_log[-1] + "+"
    for i, notation in enumerate(gs.chess_log[j * 43 - j:]):
        if i % 2 == 0:
            log_text = log.render(
                str((j * 43) // 2 + i // 2 + 1) + '.', False, (239, 240, 209))
            screen.blit(log_text, (WIDTH_TABLE + (HIGHT - HEIGHT_TABLE) +
                        SQUARE_SIZE * 0.1, SQUARE_SIZE + size // 2 * i))
            log_text = log.render(notation, False, (239, 240, 209))
            screen.blit(log_text, (WIDTH_TABLE + (HIGHT - HEIGHT_TABLE) +
                        SQUARE_SIZE * 0.5, SQUARE_SIZE + size // 2 * i))
        else:
            log_text = log.render(notation, False, (239, 240, 209))
            screen.blit(log_text, (WIDTH_TABLE + (HIGHT - HEIGHT_TABLE) +
                        SQUARE_SIZE * 1.6, SQUARE_SIZE + size // 2 * (i - 1)))


def draw_game_state(gs, screen, valid_moves, square_selected):
    draw_board(screen)
    highlight(screen, gs, valid_moves, square_selected)
    draw_piaces(screen, gs)
    draw_description(screen)
    end_game(screen, gs)


def animate_move(move, screen, gs, clock):
    colors = ((239, 240, 209), (107, 156, 79))
    d_r = move.end_row - move.start_row
    d_c = move.end_col - move.start_col
    frame_per_second = 2
    frame_count = max(abs(d_c), abs(d_r)) * frame_per_second
    for frame in range(frame_count + 1):
        r, c = (move.start_row + d_r * frame / frame_count,
                move.start_col + d_c * frame / frame_count)
        draw_board(screen)
        draw_piaces(screen, gs)
        draw_description(screen)
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect((move.end_col * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2),
                            move.end_row * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2), SQUARE_SIZE, SQUARE_SIZE))
        p.draw.rect(screen, color, end_square)
        if move.piece_captured != "--":
            screen.blit(IMAGES[move.piece_captured], end_square)
        screen.blit(IMAGES[move.piece_moved], (c * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2),
                    r * SQUARE_SIZE + ((HIGHT - HEIGHT_TABLE) // 2), SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HIGHT))
    p.display.set_caption("Chess")
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    gs = chess_engine.Game_State()
    valid_moves = gs.get_valid_moves()
    move_made = False
    animate = False
    undo = False
    load_images()
    square_selected = ()
    player_clicks = []
    player_one = True
    player_two = False
    while True:
        human_turn = (gs.white_to_move and player_one) or (
            not gs.white_to_move and player_two)
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    if len(gs.move_log) > 0:
                        if player_one ^ player_two:
                            gs.undo_move(True)
                            gs.undo_move(True)
                        else:
                            gs.undo_move(True)
                        move_made = True
                        animate = False
                        square_selected = ()
                        player_clicks = []
                elif event.key == p.K_x:
                    if len(gs.move_undo_log) > 0:
                        gs.undo_undo_move()
                        # pawn promotion
                        if gs.move_log[-1].start_row == 1 and gs.move_log[-1].end_row == 0 and gs.board[gs.move_log[-1].end_row][gs.move_log[-1].end_col] == "wp":
                            screen.blit(IMAGES["wQ"], ((
                                HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 0, 5, 40, 40))
                            screen.blit(IMAGES["wR"], ((
                                HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1, 5, 40, 40))
                            screen.blit(IMAGES["wB"], ((
                                HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2, 5, 40, 40))
                            screen.blit(IMAGES["wN"], ((
                                HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3, 5, 40, 40))
                            animate_move(gs.move_log[-1], screen, gs, clock)
                            p.event.clear()
                            while True:
                                event_ = p.event.wait()
                                if event_.type == p.MOUSEBUTTONDOWN:
                                    location_ = p.mouse.get_pos()
                                    if (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 0 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1:
                                        if 5 <= location_[1] <= 40 + 5:
                                            gs.board[gs.move_log[-1].end_row][gs.move_log[-1].end_col] = "wQ"
                                            break
                                    elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2:
                                        if 5 <= location_[1] <= 40 + 5:
                                            gs.board[gs.move_log[-1].end_row][gs.move_log[-1].end_col] = "wR"
                                            break
                                    elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3:
                                        if 5 <= location_[1] <= 40 + 5:
                                            gs.board[gs.move_log[-1].end_row][gs.move_log[-1].end_col] = "wB"
                                            break
                                    elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 4:
                                        if 5 <= location_[1] <= 40 + 5:
                                            gs.board[gs.move_log[-1].end_row][gs.move_log[-1].end_col] = "wN"
                                            break
                                elif event_.type == p.KEYDOWN:
                                    if event_.key == p.K_z:
                                        if len(gs.move_log) > 0:
                                            if player_one ^ player_two:
                                                gs.undo_move(True)
                                                gs.undo_move(True)
                                            else:
                                                gs.undo_move(True)
                                        break
                                elif event_.type == p.QUIT:
                                    p.quit()
                                    sys.exit()

                                else:
                                    p.event.clear()
                        elif gs.move_log[-1].start_row == 6 and gs.move_log[-1].end_row == 7 and gs.board[gs.move_log[-1].end_row][gs.move_log[-1].end_col] == "bp":
                            screen.blit(IMAGES["bQ"], ((
                                HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 0, 5, 40, 40))
                            screen.blit(IMAGES["bR"], ((
                                HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1, 5, 40, 40))
                            screen.blit(IMAGES["bB"], ((
                                HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2, 5, 40, 40))
                            screen.blit(IMAGES["bN"], ((
                                HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3, 5, 40, 40))
                            animate_move(gs.move_log[-1], screen, gs, clock)
                            p.event.clear()
                            while True:
                                event_ = p.event.wait()
                                if event_.type == p.MOUSEBUTTONDOWN:
                                    location_ = p.mouse.get_pos()
                                    if (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 0 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1:
                                        if 5 <= location_[1] <= 40 + 5:
                                            gs.board[gs.move_log[-1].end_row][gs.move_log[-1].end_col] = "bQ"
                                            break
                                    elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2:
                                        if 5 <= location_[1] <= 40 + 5:
                                            gs.board[gs.move_log[-1].end_row][gs.move_log[-1].end_col] = "bR"
                                            break
                                    elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3:
                                        if 5 <= location_[1] <= 40 + 5:
                                            gs.board[gs.move_log[-1].end_row][gs.move_log[-1].end_col] = "bB"
                                            break
                                    elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 4:
                                        if 5 <= location_[1] <= 40 + 5:
                                            gs.board[gs.move_log[-1].end_row][gs.move_log[-1].end_col] = "bN"
                                            break
                                elif event_.type == p.KEYDOWN:
                                    if event_.key == p.K_z:
                                        if len(gs.move_log) > 0:
                                            if player_one ^ player_two:
                                                gs.undo_move(True)
                                                gs.undo_move(True)
                                            else:
                                                gs.undo_move(True)
                                        break
                                elif event_.type == p.QUIT:
                                    p.quit()
                                    sys.exit()

                                else:
                                    p.event.clear()
                        move_made = True
                        animate = False
                        square_selected = ()
                        player_clicks = []
                elif event.key == p.K_r:
                    gs = chess_engine.Game_State()
                    valid_moves = gs.get_valid_moves()
                    move_made = False
                    animate = False
                    undo = False
                    square_selected = ()
                    player_clicks = []
            elif event.type == p.MOUSEBUTTONDOWN:
                if not gs.checkmate and not gs.stalemate and human_turn:
                    location = p.mouse.get_pos()
                    if ((HIGHT - HEIGHT_TABLE) // 2) <= location[0] <= ((HIGHT - HEIGHT_TABLE) // 2) + SQUARE_SIZE * DIMENSION:
                        if ((HIGHT - HEIGHT_TABLE) // 2) <= location[1] <= ((HIGHT - HEIGHT_TABLE) // 2) + SQUARE_SIZE * DIMENSION:
                            col = location[0] // SQUARE_SIZE
                            row = location[1] // SQUARE_SIZE
                            if not player_clicks:
                                if (gs.board[row][col][0] == "w" and gs.white_to_move) or (gs.board[row][col][0] == "b" and not gs.white_to_move):
                                    square_selected = (row, col)
                                    player_clicks.append(square_selected)
                            else:
                                player_clicks.append((row, col))
                                move = chess_engine.Move(
                                    player_clicks[0], player_clicks[1], gs.board)
                                if move in valid_moves:
                                    gs.make_move(move, True, True)
                                    # pawn promotion
                                    if player_clicks[0][0] == 1 and player_clicks[1][0] == 0 and gs.board[player_clicks[1][0]][player_clicks[1][1]] == "wp":
                                        screen.blit(IMAGES["wQ"], ((
                                            HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 0, 5, 40, 40))
                                        screen.blit(IMAGES["wR"], ((
                                            HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1, 5, 40, 40))
                                        screen.blit(IMAGES["wB"], ((
                                            HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2, 5, 40, 40))
                                        screen.blit(IMAGES["wN"], ((
                                            HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3, 5, 40, 40))
                                        animate_move(
                                            gs.move_log[-1], screen, gs, clock)
                                        p.event.clear()
                                        while True:
                                            event_ = p.event.wait()
                                            if event_.type == p.MOUSEBUTTONDOWN:
                                                location_ = p.mouse.get_pos()
                                                if (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 0 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1:
                                                    if 5 <= location_[1] <= 40 + 5:
                                                        gs.board[player_clicks[1][0]
                                                                 ][player_clicks[1][1]] = "wQ"
                                                        undo = True
                                                        break
                                                elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2:
                                                    if 5 <= location_[1] <= 40 + 5:
                                                        gs.board[player_clicks[1][0]
                                                                 ][player_clicks[1][1]] = "wR"
                                                        undo = True
                                                        break
                                                elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3:
                                                    if 5 <= location_[1] <= 40 + 5:
                                                        gs.board[player_clicks[1][0]
                                                                 ][player_clicks[1][1]] = "wB"
                                                        undo = True
                                                        break
                                                elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 4:
                                                    if 5 <= location_[1] <= 40 + 5:
                                                        gs.board[player_clicks[1][0]
                                                                 ][player_clicks[1][1]] = "wN"
                                                        undo = True
                                                        break
                                            elif event_.type == p.KEYDOWN:
                                                if event_.key == p.K_z:
                                                    if len(gs.move_log) > 0:
                                                        if player_one ^ player_two:
                                                            gs.undo_move(True)
                                                            gs.undo_move(True)
                                                        else:
                                                            gs.undo_move(True)
                                                        undo = True
                                                    break
                                            elif event_.type == p.QUIT:
                                                p.quit()
                                                sys.exit()

                                            else:
                                                p.event.clear()
                                    elif player_clicks[0][0] == 6 and player_clicks[1][0] == 7 and gs.board[player_clicks[1][0]][player_clicks[1][1]] == "bp":
                                        screen.blit(IMAGES["bQ"], ((
                                            HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 0, 5, 40, 40))
                                        screen.blit(IMAGES["bR"], ((
                                            HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1, 5, 40, 40))
                                        screen.blit(IMAGES["bB"], ((
                                            HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2, 5, 40, 40))
                                        screen.blit(IMAGES["bN"], ((
                                            HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3, 5, 40, 40))
                                        animate_move(
                                            gs.move_log[-1], screen, gs, clock)
                                        p.event.clear()
                                        while True:
                                            event_ = p.event.wait()
                                            if event_.type == p.MOUSEBUTTONDOWN:
                                                location_ = p.mouse.get_pos()
                                                if (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 0 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1:
                                                    if 5 <= location_[1] <= 40 + 5:
                                                        gs.board[player_clicks[1][0]
                                                                 ][player_clicks[1][1]] = "bQ"
                                                        undo = True
                                                        break
                                                elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 1 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2:
                                                    if 5 <= location_[1] <= 40 + 5:
                                                        gs.board[player_clicks[1][0]
                                                                 ][player_clicks[1][1]] = "bR"
                                                        undo = True
                                                        break
                                                elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 2 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3:
                                                    if 5 <= location_[1] <= 40 + 5:
                                                        gs.board[player_clicks[1][0]
                                                                 ][player_clicks[1][1]] = "bB"
                                                        undo = True
                                                        break
                                                elif (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 3 <= location_[0] <= (HIGHT - HEIGHT_TABLE) // 4 + SQUARE_SIZE * 8 + 45 * 4:
                                                    if 5 <= location_[1] <= 40 + 5:
                                                        gs.board[player_clicks[1][0]
                                                                 ][player_clicks[1][1]] = "bN"
                                                        undo = True
                                                        break
                                            elif event_.type == p.KEYDOWN:
                                                if event_.key == p.K_z:
                                                    if len(gs.move_log) > 0:
                                                        if player_one ^ player_two:
                                                            gs.undo_move(True)
                                                            gs.undo_move(True)
                                                        else:
                                                            gs.undo_move(True)
                                                        undo = True
                                                    break
                                            elif event_.type == p.QUIT:
                                                p.quit()
                                                sys.exit()

                                            else:
                                                p.event.clear()
                                    move_made = True
                                    animate = True
                                    if undo:
                                        animate = False
                                        undo = False
                                    square_selected = ()
                                    player_clicks = []
                                else:
                                    if (gs.board[row][col][0] == "w" and gs.white_to_move) or (gs.board[row][col][0] == "b" and not gs.white_to_move):
                                        square_selected = (row, col)
                                        player_clicks = []
                                        player_clicks.append(square_selected)
                                    else:
                                        square_selected = ()
                                        player_clicks = []

        if not gs.checkmate and not gs.stalemate and not human_turn:
            ai_move = ai.negamax_ab_helper(gs, valid_moves)
            if ai_move is None:
                ai_move = ai.find_randome_move(valid_moves)
            gs.make_move(ai_move, False, True)
            move_made = True
            animate = True
        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs, clock)
            screen.fill(p.Color("black"))
            valid_moves = gs.get_valid_moves()
            move_made = False
            draw_log(screen, gs)
        gs.check = False
        draw_game_state(gs, screen, valid_moves, square_selected)

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
