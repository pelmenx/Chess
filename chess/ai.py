import random

PIECE_SCORE = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 10000
STALEMATE = 0
DEPTH = 2


def find_randome_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


def negamax_ab_helper(gs, valid_moves):
    global next_move, counter
    counter = 0
    next_move = None
    random.shuffle(valid_moves)
    negamax_ab(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.white_to_move else -1)
    print(counter)
    return next_move


def negamax_ab(gs, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move, counter
    counter += 1
    if depth == 0:
        return turn_multiplier * score_board(gs)

    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        random.shuffle(next_moves)
        score = -negamax_ab(gs, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score


def score_board(gs):
    if gs.checkmate:
        if gs.white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    if gs.stalemate:
        return STALEMATE
    score = 0
    for row in gs.board:
        for item in row:
            if item != "--":
                if item[0] == "w":
                    score += PIECE_SCORE[item[1]]
                else:
                    score -= PIECE_SCORE[item[1]]
    return score
