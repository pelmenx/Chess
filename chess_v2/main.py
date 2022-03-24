import pygame as p
import sys
from pathlib import Path
import chess_engine


WIDTH = 712
HEIGHT = 522
WIDTH_TABLE = 512
HEIGHT_TABLE = 512
BOARDER = (HEIGHT - HEIGHT_TABLE) // 2
DIMENSION = 8
SQUARE_SIZE = WIDTH_TABLE // DIMENSION
FPS = 30
IMAGES = {}


def load_images():
    pieces = ["10", "11", "12", "13", "14",
              "15", "20", "21", "22", "23", "24", "25"]
    for piece in pieces:
        path = Path(Path.cwd(), "Chess", "chess_v2", "images", f"{piece}.png")
        IMAGES[piece] = p.transform.scale(
            p.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))


def draw_board(screen):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if (i + j) % 2 == 1:
                p.draw.rect(screen, (107, 156, 79), (i * SQUARE_SIZE + BOARDER,
                            j * SQUARE_SIZE + BOARDER, SQUARE_SIZE, SQUARE_SIZE))
            else:
                p.draw.rect(screen, (239, 240, 209), (i * SQUARE_SIZE + BOARDER,
                            j * SQUARE_SIZE + BOARDER, SQUARE_SIZE, SQUARE_SIZE))


def draw_description(screen):
    columns = ("a", "b", "c", "d", "e", "f", "g", "h")
    description = p.font.Font(None, int(SQUARE_SIZE * 0.25))
    for i in range(DIMENSION):
        white_description = description.render(
            str(DIMENSION - i), False, (239, 240, 209))
        green_description = description.render(
            str(DIMENSION - i), False, (107, 156, 79))
        if i % 2 == 1:
            screen.blit(white_description, (BOARDER*2,
                        i * SQUARE_SIZE + BOARDER*2))
        else:
            screen.blit(green_description, (BOARDER*2,
                        i * SQUARE_SIZE + BOARDER*2))
    for j in range(DIMENSION):
        white_description = description.render(
            columns[j], False, (239, 240, 209))
        green_description = description.render(
            columns[j], False, (107, 156, 79))
        if j % 2 == 0:
            screen.blit(white_description, (j * SQUARE_SIZE + BOARDER*2 + SQUARE_SIZE *
                        0.75, (DIMENSION - 1) * SQUARE_SIZE + BOARDER*2 + SQUARE_SIZE * 0.7))
        else:
            screen.blit(green_description, (j * SQUARE_SIZE + BOARDER*2 + SQUARE_SIZE *
                        0.75, (DIMENSION - 1) * SQUARE_SIZE + BOARDER*2 + SQUARE_SIZE * 0.7))


def draw_pieces(screen, gs):
    for i, row in enumerate(gs.board):
        for j, piece in enumerate(row):
            if piece != 0:
                screen.blit(IMAGES[str(piece)], (j * SQUARE_SIZE + BOARDER,
                            i * SQUARE_SIZE + BOARDER, SQUARE_SIZE, SQUARE_SIZE))


def draw_possible_moves(screen, square_selected, gs):
    if not square_selected:
        return
    r, c = square_selected
    if (gs.white_to_move and gs.board[r][c] in gs.white_pieces) or (not gs.white_to_move and gs.board[r][c] in gs.black_pieces):
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("yellow"))
        screen.blit(s, (c * SQUARE_SIZE + BOARDER,
                    r * SQUARE_SIZE + BOARDER))
        s.fill((0, 0, 0, 255))
        s.set_alpha(150)
        for move in gs.valid_moves:
            if move.start_row == r and move.start_col == c:
                if gs.board[move.end_row][move.end_col] == 0:
                    if (move.end_col + move.end_row) % 2 == 1:
                        p.draw.circle(screen, (96, 141, 70), (move.end_col * SQUARE_SIZE + BOARDER + SQUARE_SIZE //
                                      2, move.end_row * SQUARE_SIZE + BOARDER + SQUARE_SIZE // 2), SQUARE_SIZE * 0.2)
                    else:
                        p.draw.circle(screen, (214, 217, 188), (move.end_col * SQUARE_SIZE + BOARDER + SQUARE_SIZE //
                                      2, move.end_row * SQUARE_SIZE + BOARDER + SQUARE_SIZE // 2), SQUARE_SIZE * 0.2)
                elif (move.end_col + move.end_row) % 2 == 1:
                    p.draw.circle(screen, (96, 141, 70), (move.end_col * SQUARE_SIZE + BOARDER + SQUARE_SIZE //
                                  2, move.end_row * SQUARE_SIZE + BOARDER + SQUARE_SIZE // 2), SQUARE_SIZE * 0.5, 5)
                else:
                    p.draw.circle(screen, (214, 217, 188), (move.end_col * SQUARE_SIZE + BOARDER + SQUARE_SIZE //
                                  2, move.end_row * SQUARE_SIZE + BOARDER + SQUARE_SIZE // 2), SQUARE_SIZE * 0.5, 5)


def draw_game_state(screen, gs, clicks):
    draw_board(screen)
    draw_description(screen)
    draw_pieces(screen, gs)
    if clicks:
        draw_possible_moves(screen, clicks[0], gs)


def main():
    gs = chess_engine.GameState()
    load_images()
    p.init()
    clicks = []
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill("black")
    clock = p.time.Clock()
    draw_game_state(screen, gs, clicks)
    p.display.set_caption("Chess")
    while True:
        if not gs.valid_moves:
            gs.all_possible_moves()
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                x, y = p.mouse.get_pos()
                if BOARDER < x < BOARDER + WIDTH_TABLE and BOARDER < y < BOARDER + HEIGHT_TABLE:
                    if not clicks:
                        clicks.append(((y-BOARDER)//SQUARE_SIZE,
                                      (x-BOARDER)//SQUARE_SIZE))
                    elif clicks:
                        clicks.append(((y-BOARDER)//SQUARE_SIZE,
                                      (x-BOARDER)//SQUARE_SIZE))
                    if len(clicks) == 2:
                        move = chess_engine.Move(clicks, gs)
                        if move in gs.valid_moves:
                            gs.make_move(move)
                            clicks.clear()
                        else:
                            row, col = clicks[1]
                            if (gs.board[row][col] in gs.white_pieces and gs.white_to_move) or (gs.board[row][col] in gs.black_pieces and not gs.white_to_move):
                                clicks = [clicks[-1]]
                            else:
                                clicks.clear()
            if event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    gs.undo_move()
                elif event.key == p.K_x:
                    gs.yield_move()
        draw_game_state(screen, gs, clicks)
        clock.tick(FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
