def opponent(player):
    return BLACK if player is WHITE else WHITE

def minimax(player, board, depth, evaluate):
    def value(board):
        return -minimax(opponent(player), board, depth - 1, evaluate)[0]

    if depth == 0:
        return evaluate(player, board), None
    moves = legal_moves(player, board)
    if not moves:
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), Non
        return value(board), None

    return max((value(make_move(m, player, list(board))), m) for m in moves)

MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE

def final_value(player, board):
#
    diff = score(player, board)
    if diff < 0:
        return MIN_VALUE
    elif diff > 0:
        return MAX_VALUE
    return diff

def minimax_searcher(depth, evaluate):
#
    def strategy(player, board):
        return minimax(player, board, depth, evaluate)[1]
    return strategy
