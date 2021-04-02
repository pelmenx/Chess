class Game_State(object):
    def __init__(self):
        # board representation
        # "w" - white peaces, "b" - black piaces
        # "R" - rock, "N" - knight, "B" - bishop, "Q" - queen, "K" - king, "p" - pawn , "--" - free square
        self.board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                      ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.white_to_move = True
        self.move_log = []
        self.move_undo_log = []
        self.chess_log = []
        self.chess_undo_log = []
        self.white_king_position = [(7, 4)]
        self.black_king_position = [(0, 4)]
        self.left_white_rock_position = [(7, 0)]
        self.right_white_rock_position = [(7, 7)]
        self.left_black_rock_position = [(0, 0)]
        self.right_black_rock_position = [(0, 7)]
        self.checkmate = False
        self.stalemate = False
        self.check = False

    def make_move(self, move, human=False, is_turn=False):
        if is_turn:
            self.move_undo_log = []
            self.chess_log.append(move.get_chess_notation(self))
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        # track king position
        if move.piece_moved == "wK":
            self.white_king_position.append((move.end_row, move.end_col))
            if move.start_row == 7 and move.start_col == 4:
                if move.end_row == 7 and move.end_col == 6:
                    self.board[7][7] = "--"
                    self.board[7][5] = "wR"
                    self.right_white_rock_position.append((7, 5))
                elif move.end_row == 7 and move.end_col == 2:
                    self.board[7][0] = "--"
                    self.board[7][3] = "wR"
                    self.left_white_rock_position.append((7, 3))
        elif move.piece_moved == "bK":
            self.black_king_position.append((move.end_row, move.end_col))
            if move.start_row == 0 and move.start_col == 4:
                if move.end_row == 0 and move.end_col == 6:
                    self.board[0][7] = "--"
                    self.board[0][5] = "bR"
                    self.right_black_rock_position.append((0, 5))
                elif move.end_row == 0 and move.end_col == 2:
                    self.board[0][0] = "--"
                    self.board[0][3] = "bR"
                    self.left_black_rock_position.append((0, 3))
        # track rock position
        elif move.piece_moved == "wR" and len(self.white_king_position) == 1:
            if (move.start_row, move.start_col) == self.left_white_rock_position[-1]:
                self.left_white_rock_position.append((move.end_row, move.end_col))
            elif (move.start_row, move.start_col) == self.right_white_rock_position[-1]:
                self.right_white_rock_position.append((move.end_row, move.end_col))
        elif move.piece_moved == "bR" and len(self.black_king_position) == 1:
            if (move.start_row, move.start_col) == self.left_black_rock_position[-1]:
                self.left_black_rock_position.append((move.end_row, move.end_col))
            elif (move.start_row, move.start_col) == self.right_black_rock_position[-1]:
                self.right_black_rock_position.append((move.end_row, move.end_col))
        # pawn promotion
        elif move.piece_moved == "wp" and move.end_row == 0 and not human:
            self.board[move.end_row][move.end_col] = move.promotion
        elif move.piece_moved == "bp" and move.end_row == 7 and not human:
            self.board[move.end_row][move.end_col] = move.promotion
        # en passant
        elif move.piece_moved == "wp" and move.start_row == 3:
            if self.move_log[-1].piece_moved == "bp" and self.move_log[-1].start_row == 1 and self.move_log[-1].end_row == 3:
                if self.move_log[-1].start_col == move.end_col:
                    self.board[move.start_row][move.end_col] = "--"
        elif move.piece_moved == "bp" and move.start_row == 4:
            if self.move_log[-1].piece_moved == "wp" and self.move_log[-1].start_row == 6 and self.move_log[-1].end_row == 4:
                if self.move_log[-1].start_col == move.end_col:
                    self.board[move.start_row][move.end_col] = "--"

        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self, is_turn=False):
        if len(self.move_log) > 0:
            move = self.move_log.pop()
            if is_turn:
                self.move_undo_log.append(move)
                self.chess_log.pop()
            # track king position
            if move.piece_moved == "wK":
                self.white_king_position.pop()
                if move.start_row == 7 and move.start_col == 4:
                    if move.end_row == 7 and move.end_col == 6:
                        self.board[7][7] = "wR"
                        self.board[7][5] = "--"
                        self.right_white_rock_position.pop()
                    elif move.end_row == 7 and move.end_col == 2:
                        self.board[7][0] = "wR"
                        self.board[7][3] = "--"
                        self.left_white_rock_position.pop()
            elif move.piece_moved == "bK":
                self.black_king_position.pop()
                if move.start_row == 0 and move.start_col == 4:
                    if move.end_row == 0 and move.end_col == 6:
                        self.board[0][7] = "bR"
                        self.board[0][5] = "--"
                        self.right_black_rock_position.pop()
                    elif move.end_row == 0 and move.end_col == 2:
                        self.board[0][0] = "bR"
                        self.board[0][3] = "--"
                        self.left_black_rock_position.pop()
            # track rock position
            elif move.piece_moved == "wR" and len(self.white_king_position) == 1:
                if (move.end_row, move.end_col) == self.left_white_rock_position[-1]:
                    self.left_white_rock_position.pop()
                elif (move.end_row, move.end_col) == self.right_white_rock_position[-1]:
                    self.right_white_rock_position.pop()
            elif move.piece_moved == "bR" and len(self.black_king_position) == 1:
                if (move.end_row, move.end_col) == self.left_black_rock_position[-1]:
                    self.left_black_rock_position.pop()
                elif (move.end_row, move.end_col) == self.right_black_rock_position[-1]:
                    self.right_black_rock_position.pop()
            # el passant
            elif move.piece_moved == "wp" and move.start_row == 3:
                if self.move_log[-1].piece_moved == "bp" and self.move_log[-1].start_row == 1 and self.move_log[-1].end_row == 3:
                    if self.move_log[-1].start_col == move.end_col:
                        self.board[move.start_row][move.end_col] = "bp"
            elif move.piece_moved == "bp" and move.start_row == 4:
                if self.move_log[-1].piece_moved == "wp" and self.move_log[-1].start_row == 6 and self.move_log[-1].end_row == 4:
                    if self.move_log[-1].start_col == move.end_col:
                        self.board[move.start_row][move.end_col] = "wp"
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.checkmate = False
            self.stalemate = False
            self.white_to_move = not self.white_to_move

    def undo_undo_move(self):
        if len(self.move_undo_log) > 0:
            move = self.move_undo_log.pop()
            self.chess_log.append(move.get_chess_notation(self))
            self.move_log.append(move)
            self.board[move.start_row][move.start_col] = "--"
            self.board[move.end_row][move.end_col] = move.piece_moved
            # track king position
            if move.piece_moved == "wK":
                self.white_king_position.append((move.end_row, move.end_col))
                if move.start_row == 7 and move.start_col == 4:
                    if move.end_row == 7 and move.end_col == 6:
                        self.board[7][7] = "--"
                        self.board[7][5] = "wR"
                        self.right_white_rock_position.append((7, 5))
                    elif move.end_row == 7 and move.end_col == 2:
                        self.board[7][0] = "--"
                        self.board[7][3] = "wR"
                        self.left_white_rock_position.append((7, 3))
            elif move.piece_moved == "bK":
                self.black_king_position.append((move.end_row, move.end_col))
                if move.start_row == 0 and move.start_col == 4:
                    if move.end_row == 0 and move.end_col == 6:
                        self.board[0][7] = "--"
                        self.board[0][5] = "bR"
                        self.right_black_rock_position.append((0, 5))
                    elif move.end_row == 0 and move.end_col == 2:
                        self.board[0][0] = "--"
                        self.board[0][3] = "bR"
                        self.left_black_rock_position.append((0, 3))
            # track rock position
            elif move.piece_moved == "wR" and len(self.white_king_position) == 1:
                if (move.start_row, move.start_col) == self.left_white_rock_position[-1]:
                    self.left_white_rock_position.append((move.end_row, move.end_col))
                elif (move.start_row, move.start_col) == self.right_white_rock_position[-1]:
                    self.right_white_rock_position.append((move.end_row, move.end_col))
            elif move.piece_moved == "bR" and len(self.black_king_position) == 1:
                if (move.start_row, move.start_col) == self.left_black_rock_position[-1]:
                    self.left_black_rock_position.append((move.end_row, move.end_col))
                elif (move.start_row, move.start_col) == self.right_black_rock_position[-1]:
                    self.right_black_rock_position.append((move.end_row, move.end_col))
            # el passant
            elif move.piece_moved == "wp" and move.start_row == 3:
                if self.move_log[-1].piece_moved == "wp" and self.move_log[-1].start_row == 3 and self.move_log[-1].end_row == 2:
                    if self.move_log[-1].start_col == move.start_col and self.move_log[-1].end_col == move.end_col:
                        self.board[move.start_row][move.end_col] = "--"
            elif move.piece_moved == "bp" and move.start_row == 4:
                if self.move_log[-1].piece_moved == "bp" and self.move_log[-1].start_row == 4 and self.move_log[-1].end_row == 5:
                    if self.move_log[-1].start_col == move.start_col and self.move_log[-1].end_col == move.end_col:
                        self.board[move.start_row][move.end_col] = "--"
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        moves = self.get_all_possible_moves()
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if moves[i].piece_moved == "wK" and moves[i].start_row == 7 and moves[i].end_row == 7 and moves[i].start_col == 4 and moves[i].end_col == 2 and self.square_under_attack(moves[i].start_row, moves[i].start_col, moves[i].start_col - 1, moves[i].end_col):
                moves.remove(moves[i])
            elif moves[i].piece_moved == "wK" and moves[i].start_row == 7 and moves[i].end_row == 7 and moves[i].start_col == 4 and moves[i].end_col == 6 and self.square_under_attack(moves[i].start_row, moves[i].start_col, moves[i].start_col + 1, moves[i].end_col):
                moves.remove(moves[i])
            elif moves[i].piece_moved == "bK" and moves[i].start_row == 0 and moves[i].end_row == 0 and moves[i].start_col == 4 and moves[i].end_col == 2 and self.square_under_attack(moves[i].start_row, moves[i].start_col, moves[i].start_col - 1, moves[i].end_col):
                moves.remove(moves[i])
            elif moves[i].piece_moved == "bK" and moves[i].start_row == 0 and moves[i].end_row == 0 and moves[i].start_col == 4 and moves[i].end_col == 6 and self.square_under_attack(moves[i].start_row, moves[i].start_col, moves[i].start_col + 1, moves[i].end_col):
                moves.remove(moves[i])
            elif self.in_check():
                moves.remove(moves[i])
                self.check = True
            self.white_to_move = not self.white_to_move
            self.undo_move()

        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
            self.check = False
        return moves

    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_position[-1][0], self.white_king_position[-1][1])
        else:
            return self.square_under_attack(self.black_king_position[-1][0], self.black_king_position[-1][1])

    def square_under_attack(self, r, c, c1=None, c2=None):
        self.white_to_move = not self.white_to_move
        opponents_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opponents_moves:
            if move.end_row == r and move.end_col == c:
                return True
            if c1:
                if move.end_row == r and move.end_col == c1:
                    return True
                if move.end_row == r and move.end_col == c2:
                    return True
        return False

    def get_all_possible_moves(self):
        moves = []
        for i, row in enumerate(self.board):
            for j, item in enumerate(row):
                turn = self.board[i][j][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[i][j][1]
                    if piece == "p":
                        moves.extend(self.get_pawn_moves(i, j))
                    elif piece == "R":
                        moves.extend(self.get_rock_moves(i, j, turn))
                    elif piece == "N":
                        moves.extend(self.get_knight_moves(i, j, turn))
                    elif piece == "B":
                        moves.extend(self.get_bishop_moves(i, j, turn))
                    elif piece == "Q":
                        moves.extend(self.get_queen_moves(i, j, turn))
                    elif piece == "K":
                        moves.extend(self.get_king_moves(i, j, turn))
        return moves

    def get_pawn_moves(self, i, j):
        pawn_moves = []
        if self.board[i][j][0] == "w":
            if 0 <= i - 1:
                if 0 <= j - 1 and self.board[i - 1][j - 1][0] == "b":
                    if i == 1:
                        pawn_moves.append(Move((i, j), (i - 1, j - 1), self.board, "wQ"))
                        pawn_moves.append(Move((i, j), (i - 1, j - 1), self.board, "wB"))
                        pawn_moves.append(Move((i, j), (i - 1, j - 1), self.board, "wR"))
                        pawn_moves.append(Move((i, j), (i - 1, j - 1), self.board, "wN"))
                    else:
                        pawn_moves.append(Move((i, j), (i - 1, j - 1), self.board))
                if j + 1 < 8 and self.board[i - 1][j + 1][0] == "b":
                    if i == 1:
                        pawn_moves.append(Move((i, j), (i - 1, j + 1), self.board, "wQ"))
                        pawn_moves.append(Move((i, j), (i - 1, j + 1), self.board, "wB"))
                        pawn_moves.append(Move((i, j), (i - 1, j + 1), self.board, "wR"))
                        pawn_moves.append(Move((i, j), (i - 1, j + 1), self.board, "wN"))
                    else:
                        pawn_moves.append(Move((i, j), (i - 1, j + 1), self.board))
            if i == 6:
                if self.board[i - 1][j] == "--":
                    pawn_moves.append(Move((i, j), (i - 1, j), self.board))
                if self.board[i - 1][j] == "--" and self.board[i - 2][j] == "--":
                    pawn_moves.append(Move((i, j), (i - 2, j), self.board))
            else:
                if i - 1 >= 0 and self.board[i - 1][j] == "--":
                    if i == 1:
                        pawn_moves.append(Move((i, j), (i - 1, j), self.board, "wQ"))
                        pawn_moves.append(Move((i, j), (i - 1, j), self.board, "wB"))
                        pawn_moves.append(Move((i, j), (i - 1, j), self.board, "wR"))
                        pawn_moves.append(Move((i, j), (i - 1, j), self.board, "wN"))
                    else:
                        pawn_moves.append(Move((i, j), (i - 1, j), self.board))
            if i == 3:
                if self.move_log[-1].piece_moved == "bp" and self.move_log[-1].start_row == 1 and self.move_log[-1].end_row == 3:
                    if self.move_log[-1].start_col == j - 1:
                        pawn_moves.append(Move((i, j), (i - 1, j - 1), self.board))
                    elif self.move_log[-1].start_col == j + 1:
                        pawn_moves.append(Move((i, j), (i - 1, j + 1), self.board))

        else:
            if i + 1 < 8:
                if 0 <= j - 1 and self.board[i + 1][j - 1][0] == "w":
                    if i == 6:
                        pawn_moves.append(Move((i, j), (i + 1, j - 1), self.board, "bQ"))
                        pawn_moves.append(Move((i, j), (i + 1, j - 1), self.board, "bB"))
                        pawn_moves.append(Move((i, j), (i + 1, j - 1), self.board, "bR"))
                        pawn_moves.append(Move((i, j), (i + 1, j - 1), self.board, "bN"))
                    else:
                        pawn_moves.append(Move((i, j), (i + 1, j - 1), self.board))
                if j + 1 < 8 and self.board[i + 1][j + 1][0] == "w":
                    if i == 6:
                        pawn_moves.append(Move((i, j), (i + 1, j + 1), self.board, "bQ"))
                        pawn_moves.append(Move((i, j), (i + 1, j + 1), self.board, "bB"))
                        pawn_moves.append(Move((i, j), (i + 1, j + 1), self.board, "bR"))
                        pawn_moves.append(Move((i, j), (i + 1, j + 1), self.board, "bN"))
                    else:
                        pawn_moves.append(Move((i, j), (i + 1, j + 1), self.board))
            if i == 1:
                if self.board[i + 1][j] == "--":
                    pawn_moves.append(Move((i, j), (i + 1, j), self.board))
                if self.board[i + 1][j] == "--" and self.board[i + 2][j] == "--":
                    pawn_moves.append(Move((i, j), (i + 2, j), self.board))
            else:
                if i + 1 < 8 and self.board[i + 1][j] == "--":
                    if i == 6:
                        pawn_moves.append(Move((i, j), (i + 1, j), self.board, "bQ"))
                        pawn_moves.append(Move((i, j), (i + 1, j), self.board, "bB"))
                        pawn_moves.append(Move((i, j), (i + 1, j), self.board, "bR"))
                        pawn_moves.append(Move((i, j), (i + 1, j), self.board, "bN"))
                    else:
                        pawn_moves.append(Move((i, j), (i + 1, j), self.board))
            if i == 4:
                if self.move_log[-1].piece_moved == "wp" and self.move_log[-1].start_row == 6 and self.move_log[-1].end_row == 4:
                    if self.move_log[-1].start_col == j - 1:
                        pawn_moves.append(Move((i, j), (i + 1, j - 1), self.board))
                    elif self.move_log[-1].start_col == j + 1:
                        pawn_moves.append(Move((i, j), (i + 1, j + 1), self.board))
        return(pawn_moves)

    def get_rock_moves(self, i, j, turn):
        rock_moves = []
        for r in range(i + 1, 8):
            if self.board[r][j] == "--":
                rock_moves.append(Move((i, j), (r, j), self.board))
            elif self.board[r][j][0] != turn:
                rock_moves.append(Move((i, j), (r, j), self.board))
                break
            else:
                break

        for r in range(i - 1, -1, -1):
            if self.board[r][j] == "--":
                rock_moves.append(Move((i, j), (r, j), self.board))
            elif self.board[r][j][0] != turn:
                rock_moves.append(Move((i, j), (r, j), self.board))
                break
            else:
                break

        for c in range(j + 1, 8):
            if self.board[i][c] == "--":
                rock_moves.append(Move((i, j), (i, c), self.board))
            elif self.board[i][c][0] != turn:
                rock_moves.append(Move((i, j), (i, c), self.board))
                break
            else:
                break

        for c in range(j - 1, -1, -1):
            if self.board[i][c] == "--":
                rock_moves.append(Move((i, j), (i, c), self.board))
            elif self.board[i][c][0] != turn:
                rock_moves.append(Move((i, j), (i, c), self.board))
                break
            else:
                break
        return rock_moves

    def get_knight_moves(self, i, j, turn):
        knight_moves = []
        knight_possible_moves = [(i + 2, j + 1), (i + 2, j - 1),
                                 (i - 2, j + 1), (i - 2, j - 1),
                                 (i + 1, j + 2), (i + 1, j - 2),
                                 (i - 1, j + 2), (i - 1, j - 2)]
        for pos in knight_possible_moves:
            if 0 <= pos[0] < 8 and 0 <= pos[1] < 8 and self.board[pos[0]][pos[1]][0] != turn:
                knight_moves.append(Move((i, j), pos, self.board))
        return knight_moves

    def get_bishop_moves(self, i, j, turn):
        bishop_moves = []
        for r, c in zip(range(i + 1, 8), range(j + 1, 8)):
            if self.board[r][c] == "--":
                bishop_moves.append(Move((i, j), (r, c), self.board))
            elif self.board[r][c][0] != turn:
                bishop_moves.append(Move((i, j), (r, c), self.board))
                break
            else:
                break

        for r, c in zip(range(i - 1, -1, -1), range(j - 1, -1, -1)):
            if self.board[r][c] == "--":
                bishop_moves.append(Move((i, j), (r, c), self.board))
            elif self.board[r][c][0] != turn:
                bishop_moves.append(Move((i, j), (r, c), self.board))
                break
            else:
                break

        for r, c in zip(range(i + 1, 8), range(j - 1, -1, -1)):
            if self.board[r][c] == "--":
                bishop_moves.append(Move((i, j), (r, c), self.board))
            elif self.board[r][c][0] != turn:
                bishop_moves.append(Move((i, j), (r, c), self.board))
                break
            else:
                break

        for r, c in zip(range(i - 1, -1, -1), range(j + 1, 8)):
            if self.board[r][c] == "--":
                bishop_moves.append(Move((i, j), (r, c), self.board))
            elif self.board[r][c][0] != turn:
                bishop_moves.append(Move((i, j), (r, c), self.board))
                break
            else:
                break
        return bishop_moves

    def get_queen_moves(self, i, j, turn):
        queen_moves = []
        queen_moves.extend(self.get_bishop_moves(i, j, turn))
        queen_moves.extend(self.get_rock_moves(i, j, turn))
        return queen_moves

    def get_king_moves(self, i, j, turn):
        king_moves = []
        for r in range(i - 1, i + 2):
            if 0 <= r < 8:
                for c in range(j - 1, j + 2):
                    if 0 <= c < 8:
                        if self.board[r][c][0] != turn:
                            king_moves.append(Move((i, j), (r, c), self.board))
        if self.white_to_move:
            if len(self.white_king_position) == 1:
                if len(self.left_white_rock_position) == 1:
                    if self.board[i][j - 1] == "--":
                        if self.board[i][j - 2] == "--":
                            if self.board[i][j - 3] == "--":
                                if self.board[i][j - 4] == "wR":
                                    king_moves.append(Move((i, j), (i, j - 2), self.board))
                if len(self.right_white_rock_position) == 1:
                    if self.board[i][j + 1] == "--":
                        if self.board[i][j + 2] == "--":
                            if self.board[i][j + 3] == "wR":
                                king_moves.append(Move((i, j), (i, j + 2), self.board))
        else:
            if len(self.black_king_position) == 1:
                if len(self.left_black_rock_position) == 1:
                    if self.board[i][j - 1] == "--":
                        if self.board[i][j - 2] == "--":
                            if self.board[i][j - 3] == "--":
                                if self.board[i][j - 4] == "bR":
                                    king_moves.append(Move((i, j), (i, j - 2), self.board))
                if len(self.right_black_rock_position) == 1:
                    if self.board[i][j + 1] == "--":
                        if self.board[i][j + 2] == "--":
                            if self.board[i][j + 3] == "bR":
                                king_moves.append(Move((i, j), (i, j + 2), self.board))

        return king_moves


class Move(object):
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {7: "1", 6: "2", 5: "3", 4: "4", 3: "5", 2: "6", 1: "7", 0: "8"}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    def __init__(self, start_square, end_square, board, prom=None):
        super(Move, self).__init__()
        self.promotion = prom
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self, gs):
        text = self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
        if self.piece_moved[1] == "K":
            if self.start_col == self.end_col - 2:
                return "O-O"
            elif self.start_col == self.end_col + 2:
                return "O-O-O"
        elif self.piece_captured == "--":
            if self.piece_moved[1] == "p":
                text = text[:2] + "-" + text[2:]
            else:
                text = self.piece_moved[1] + text[:2] + "-" + text[2:]
        elif self.piece_captured != "--":
            if self.piece_moved[1] == "p":
                text = text[:2] + "x" + text[2:]
            else:
                text = self.piece_moved[1] + text[:2] + "x" + text[2:]
        if gs.checkmate:
            text = text + "#"
        return text

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
