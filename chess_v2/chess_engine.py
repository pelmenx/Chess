import numpy as np

# pool = multiprocessing.Semaphore(multiprocessing.cpu_count())


class GameState(object):
    def __init__(self) -> None:
        # 0 - space
        # 1x - white
        # 2x - black
        # x0 - pawn
        # x1 - rock
        # x2 - knight
        # x3 - bishop
        # x4 - queen
        # x5 - king
        self.board = np.array([[21, 0, 0, 0, 25, 0, 0, 21],
                               [20, 20, 20, 20, 20, 20, 20, 20],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [10, 10, 10, 10, 10, 10, 10, 10],
                               [11, 0, 0, 0, 15, 0, 0, 11]],
                              dtype=np.uint8)
        self.checkmate = False
        self.stealmate = False
        self.white_to_move = True
        self.white_left_rock = np.array([[7, 0]], dtype=np.uint8)
        self.white_right_rock = np.array([[7, 7]], dtype=np.uint8)
        self.black_left_rock = np.array([[0, 0]], dtype=np.uint8)
        self.black_right_rock = np.array([[0, 7]], dtype=np.uint8)
        self.white_king_position = np.array([[7, 4]], dtype=np.uint8)
        self.black_king_position = np.array([[0, 4]], dtype=np.uint8)
        self.log = []
        self.undo_log = []
        self.valid_moves = set()
        self.white_pieces = set([10, 11, 12, 13, 14, 15])
        self.black_pieces = set([20, 21, 22, 23, 24, 25])

    def piece_to_moves(self, piece, row, col):
        if piece == 10:
            self.white_pawn_moves(row, col)
        elif piece == 20:
            self.black_pawn_moves(row, col)
        elif piece in (11, 21):
            self.rock_moves(row, col)
        elif piece in (12, 22):
            self.knight_moves(row, col)
        elif piece in (13, 23):
            self.bishop_moves(row, col)
        elif piece in (14, 24):
            self.queen_moves(row, col)
        elif piece in (15, 25):
            self.king_moves(row, col)

    def all_possible_moves(self):
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if (piece in self.white_pieces and self.white_to_move) or (piece in self.black_pieces and not self.white_to_move):
                    self.piece_to_moves(piece, i, j)

    def make_move(self, move):
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.board[move.start_row][move.start_col] = 0
        self.white_to_move = not self.white_to_move
        self.log.append(move)
        self.undo_log = []
        self.valid_moves.clear()

        self.track_position(move, True)

    def yield_move(self):
        if self.undo_log:
            move = self.undo_log.pop()
            self.board[move.end_row][move.end_col] = move.piece_moved
            if move.piece_captured:
                self.board[move.start_row][move.start_col] = 0
            else:
                self.board[move.start_row][move.start_col] = move.piece_captured
            self.log.append(move)
            self.white_to_move = not self.white_to_move
            self.valid_moves.clear()

            self.track_position(move, True)

    def undo_move(self):
        if self.log:
            move = self.log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.undo_log.append(move)
            self.white_to_move = not self.white_to_move
            self.valid_moves.clear()

            self.track_position(move, False)

    def track_position(self, move, do):
        if do:
            if move.piece_moved in (15, 25):
                if move.piece_moved == 15:
                    self.white_king_position = np.append(self.white_king_position,
                                                         [[move.end_row, move.end_col]], axis=0)
                    if move.end_row == 7 and move.end_col == 2:
                        self.board[7][0] = 0
                        self.board[7][3] = 11
                        self.white_left_rock = np.append(self.white_left_rock,
                                                         [[7, 3]], axis=0)
                    elif move.end_row == 7 and move.end_col == 6:
                        self.board[7][7] = 0
                        self.board[7][5] = 11
                        self.white_right_rock = np.append(self.white_right_rock,
                                                          [[7, 5]], axis=0)
                elif move.piece_moved == 25:
                    self.black_king_position = np.append(self.black_king_position,
                                                         [[move.end_row, move.end_col]], axis=0)
                    if move.end_row == 0 and move.end_col == 2:
                        self.board[0][0] = 0
                        self.board[0][3] = 21
                        self.black_left_rock = np.append(self.black_left_rock,
                                                         [[0, 3]], axis=0)
                    elif move.end_row == 0 and move.end_col == 6:
                        self.board[0][7] = 0
                        self.board[0][5] = 21
                        self.black_right_rock = np.append(self.black_right_rock,
                                                          [[0, 5]], axis=0)
            elif move.piece_moved in (11, 21):
                if np.array_equal(self.white_left_rock[-1], [move.start_row, move.start_col]):
                    self.white_left_rock = np.append(self.white_left_rock,
                                                     [[move.end_row, move.end_col]], axis=0)
                elif np.array_equal(self.white_right_rock[-1], [move.start_row, move.start_col]):
                    self.white_right_rock = np.append(self.white_right_rock,
                                                      [[move.end_row, move.end_col]], axis=0)
                elif np.array_equal(self.black_left_rock[-1], [move.start_row, move.start_col]):
                    self.black_left_rock = np.append(self.black_left_rock,
                                                     [[move.end_row, move.end_col]], axis=0)
                elif np.array_equal(self.black_right_rock[-1], [move.start_row, move.start_col]):
                    self.black_right_rock = np.append(self.black_right_rock,
                                                      [[move.end_row, move.end_col]], axis=0)
        else:
            if move.piece_moved in (15, 25):
                if move.piece_moved == 15:
                    self.white_king_position = self.white_king_position[:-1]
                    if move.end_row == 7 and move.end_col == 2:
                        self.board[7][0] = 11
                        self.board[7][3] = 0
                        self.white_left_rock = self.white_left_rock[:-1]
                    elif move.end_row == 7 and move.end_col == 6:
                        self.board[7][7] = 11
                        self.board[7][5] = 0
                        self.white_right_rock = self.white_right_rock[:-1]
                elif move.piece_moved == 25:
                    self.black_king_position = self.black_king_position[:-1]
                    if move.end_row == 0 and move.end_col == 2:
                        self.board[0][0] = 21
                        self.board[0][3] = 0
                        self.black_left_rock = self.black_left_rock[:-1]
                    elif move.end_row == 0 and move.end_col == 6:
                        self.board[0][7] = 21
                        self.board[0][5] = 0
                        self.black_right_rock = self.black_right_rock[:-1]
            elif move.piece_moved in (11, 21):
                if np.array_equal(self.white_left_rock[-1], [move.end_row, move.end_col]):
                    self.white_left_rock = self.white_left_rock[:-1]
                elif np.array_equal(self.white_right_rock[-1], [move.end_row, move.end_col]):
                    self.white_right_rock = self.white_right_rock[:-1]
                elif np.array_equal(self.black_left_rock[-1], [move.end_row, move.end_col]):
                    self.black_left_rock = self.black_left_rock[:-1]
                elif np.array_equal(self.black_right_rock[-1], [move.end_row, move.end_col]):
                    self.black_right_rock = self.black_right_rock[:-1]

    def white_pawn_moves(self, row, col):
        if row > 0:
            if row == 6 and self.board[row-2][col] == 0:
                self.valid_moves.add(Move(((row, col), (row-2, col)), self))
            if self.board[row-1][col] == 0:
                self.valid_moves.add(Move(((row, col), (row-1, col)), self))
            if col+1 < len(self.board[0]) and self.board[row-1][col+1] in self.black_pieces:
                self.valid_moves.add(Move(((row, col), (row-1, col+1)), self))
            if col-1 >= 0 and self.board[row-1][col-1] in self.black_pieces:
                self.valid_moves.add(Move(((row, col), (row-1, col-1)), self))
        if row == 3:
            if self.log:
                last_move = self.log[-1]
                if last_move.piece_moved == 20 and last_move.start_row == 1 and last_move.end_row == 3 and (last_move.start_col == col-1):
                    self.valid_moves.add(
                        Move(((row, col), (row-1, col-1)), self))
                elif last_move.piece_moved == 20 and last_move.start_row == 1 and last_move.end_row == 3 and (last_move.start_col == col+1):
                    self.valid_moves.add(
                        Move(((row, col), (row-1, col+1)), self))

    def black_pawn_moves(self, row, col):
        if row < len(self.board) - 2:
            if row == 1 and self.board[row+2][col] == 0:
                self.valid_moves.add(Move(((row, col), (row+2, col)), self))
            if self.board[row+1][col] == 0:
                self.valid_moves.add(Move(((row, col), (row+1, col)), self))
            if col+1 < len(self.board[0]) and self.board[row+1][col+1] in self.white_pieces:
                self.valid_moves.add(Move(((row, col), (row+1, col+1)), self))
            if col-1 >= 0 and self.board[row+1][col-1] in self.white_pieces:
                self.valid_moves.add(Move(((row, col), (row+1, col-1)), self))
        if row == 4:
            if self.log:
                last_move = self.log[-1]
                if last_move.piece_moved == 10 and last_move.start_row == 6 and last_move.end_row == 4 and (last_move.start_col == col-1):
                    self.valid_moves.add(
                        Move(((row, col), (row+1, col-1)), self))
                elif last_move.piece_moved == 10 and last_move.start_row == 6 and last_move.end_row == 4 and (last_move.start_col == col+1):
                    self.valid_moves.add(
                        Move(((row, col), (row+1, col+1)), self))

    def rock_moves(self, row, col):
        moves = ((1, 0), (-1, 0), (0, 1), (0, -1))
        opp_pieces = self.black_pieces if self.white_to_move else self.white_pieces
        for move in moves:
            r = row + move[0]
            c = col + move[1]
            while 0 <= r < len(self.board) and 0 <= c < len(self.board[0]):
                if self.board[r][c] == 0:
                    self.valid_moves.add(Move(((row, col), (r, c)), self))
                    r += move[0]
                    c += move[1]
                else:
                    if self.board[r][c] in opp_pieces:
                        self.valid_moves.add(
                            Move(((row, col), (r, c)), self))
                    break

    def knight_moves(self, row, col):
        moves = ((-2, -1), (-2, 1), (2, -1), (2, 1),
                 (-1, -2), (-1, 2), (1, -2), (1, 2))
        self_pieces = self.white_pieces if self.white_to_move else self.black_pieces
        for move in moves:
            r = row + move[0]
            c = col + move[1]
            if 0 <= r < len(self.board) and 0 <= c < len(self.board[0]):
                if self.board[r][c] not in self_pieces:
                    self.valid_moves.add(Move(((row, col), (r, c)), self))

    def bishop_moves(self, row, col):
        moves = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        opp_pieces = self.black_pieces if self.white_to_move else self.white_pieces
        for move in moves:
            r = row + move[0]
            c = col + move[1]
            while 0 <= r < len(self.board) and 0 <= c < len(self.board[0]):
                if self.board[r][c] == 0:
                    self.valid_moves.add(Move(((row, col), (r, c)), self))
                    r += move[0]
                    c += move[1]
                else:
                    if self.board[r][c] in opp_pieces:
                        self.valid_moves.add(
                            Move(((row, col), (r, c)), self))
                    break

    def queen_moves(self, row, col):
        self.bishop_moves(row, col)
        self.rock_moves(row, col)

    def king_moves(self, row, col):
        self_pieces = self.white_pieces if self.white_to_move else self.black_pieces
        opp_king = self.black_king_position[-1] if self.white_to_move else self.white_king_position[-1]

        prohibited_moves = set()
        for r in range(opp_king[0]-1, opp_king[0]+2):
            for c in range(opp_king[1]-1, opp_king[1]+2):
                if 0 <= r < len(self.board) and 0 <= c < len(self.board[0]):
                    prohibited_moves.add((r, c))

        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if 0 <= r < len(self.board) and 0 <= c < len(self.board[0]) and (r, c) not in prohibited_moves:
                    if self.board[r][c] not in self_pieces:
                        self.valid_moves.add(Move(((row, col), (r, c)), self))

        king = self.white_king_position if self.white_to_move else self.black_king_position
        left_rock = self.white_left_rock if self.white_to_move else self.black_left_rock
        right_rock = self.white_right_rock if self.white_to_move else self.black_right_rock
        r = 7 if self.white_to_move else 0
        rock = 11 if self.white_to_move else 21
        if len(king) == 1 and len(left_rock) == 1 and self.board[r][0] == rock and not np.array_equal(right_rock[-1], [r, 0]) and sum(self.board[r][1:4]) == 0:
            self.valid_moves.add(Move(((row, col), (r, 2)), self))
        if len(king) == 1 and len(right_rock) == 1 and self.board[r][7] == rock and not np.array_equal(left_rock[-1], [r, 7]) and sum(self.board[r][5:7]) == 0:
            self.valid_moves.add(Move(((row, col), (r, 6)), self))


class Move(object):
    def __init__(self, move, gs) -> None:
        self.start_row = move[0][0]
        self.start_col = move[0][1]
        self.end_row = move[1][0]
        self.end_col = move[1][1]
        self.piece_moved = gs.board[self.start_row][self.start_col]
        self.piece_captured = gs.board[self.end_row][self.end_col]
        self.id = self.start_row * 1000 + self.start_col * \
            100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
