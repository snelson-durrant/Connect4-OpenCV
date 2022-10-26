import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER_PIECE = 1  # red
AI_PIECE = 2  # yellow

MINIMAX_DEPTH = 7


def sort_from_middle(list, reverse=False):
    if len(list) <= 1:
        return list
    tail = sorted([list[-1], list[0]], reverse=reverse)
    return sort_from_middle(list[1:-1], reverse) + tail


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def get_valid_locations(board):
    locations = []
    for c in range(COLUMN_COUNT):
        if board[ROW_COUNT - 1][c] == 0:
            locations.append(c)
    locations = sort_from_middle(locations)
    return locations


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print()
    print(np.flip(board, 0))
    print()


def four_in_a_row(board, piece):

    for c in range(COLUMN_COUNT - 3):

        # check horizontals for win
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

        for r in range(ROW_COUNT - 3):

            # check positive diagonals for win
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

            # check negative diagonals for win
            if (
                board[r + 3][c] == piece
                and board[r + 2][c + 1] == piece
                and board[r + 1][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    for c in range(COLUMN_COUNT):

        # check verticals for win
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True


def in_a_row(board, piece):
    even_threes = 0
    odd_threes = 0
    twos = 0
    ones = 0

    for c in range(COLUMN_COUNT - 3):

        for r in range(ROW_COUNT):

            # check horizontals for pattern _XXX
            if (
                board[r][c] == 0
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                if r % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check horizontals for pattern X_XX
            elif (
                board[r][c] == piece
                and board[r][c + 1] == 0
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                if r % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check horizontals for pattern XX_X
            elif (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == 0
                and board[r][c + 3] == piece
            ):
                if r % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check horizontals for pattern XXX_
            elif (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == 0
            ):
                if r % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check horizontals for pattern __XX
            elif (
                board[r][c] == 0
                and board[r][c + 1] == 0
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                twos = twos + 1

            # check horizontals for pattern X__X
            elif (
                board[r][c] == 0
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == 0
            ):
                twos = twos + 1

            # check horizontals for pattern XX__
            elif (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == 0
                and board[r][c + 3] == 0
            ):
                twos = twos + 1

            # check horizontals for pattern _XX_
            elif (
                board[r][c] == 0
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == 0
            ):
                twos = twos + 1

            # check horizontals for pattern ___X
            elif (
                board[r][c] == 0
                and board[r][c + 1] == 0
                and board[r][c + 2] == 0
                and board[r][c + 3] == piece
            ):
                ones = ones + 1

            # check horizontals for pattern X___
            elif (
                board[r][c] == piece
                and board[r][c + 1] == 0
                and board[r][c + 2] == 0
                and board[r][c + 3] == 0
            ):
                ones = ones + 1

            # check horizontals for pattern _X__
            elif (
                board[r][c] == 0
                and board[r][c + 1] == piece
                and board[r][c + 2] == 0
                and board[r][c + 3] == 0
            ):
                ones = ones + 1

            # check horizontals for pattern __X_
            elif (
                board[r][c] == 0
                and board[r][c + 1] == 0
                and board[r][c + 2] == piece
                and board[r][c + 3] == 0
            ):
                ones = ones + 1

        for r in range(ROW_COUNT - 3):

            # check positive diagonals for pattern _XXX
            if (
                board[r][c] == 0
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                if r % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check positive diagonals for pattern X_XX
            elif (
                board[r][c] == piece
                and board[r + 1][c + 1] == 0
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                if (r + 1) % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check positive diagonals for pattern XX_X
            elif (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == 0
                and board[r + 3][c + 3] == piece
            ):
                if (r + 2) % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check positive diagonals for pattern XXX_
            elif (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == 0
            ):
                if (r + 3) % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check positive diagonals for pattern __XX
            elif (
                board[r][c] == 0
                and board[r + 1][c + 1] == 0
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                twos = twos + 1

            # check positive diagonals for pattern X__X
            elif (
                board[r][c] == piece
                and board[r + 1][c + 1] == 0
                and board[r + 2][c + 2] == 0
                and board[r + 3][c + 3] == piece
            ):
                twos = twos + 1

            # check positive diagonals for pattern XX__
            elif (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == 0
                and board[r + 3][c + 3] == 0
            ):
                twos = twos + 1

            # check positive diagonals for pattern _XX_
            elif (
                board[r][c] == 0
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == 0
            ):
                twos = twos + 1

            # check positive diagonals for pattern ___X
            elif (
                board[r][c] == 0
                and board[r + 1][c + 1] == 0
                and board[r + 2][c + 2] == 0
                and board[r + 3][c + 3] == piece
            ):
                ones = ones + 1

            # check positive diagonals for pattern X___
            elif (
                board[r][c] == piece
                and board[r + 1][c + 1] == 0
                and board[r + 2][c + 2] == 0
                and board[r + 3][c + 3] == 0
            ):
                ones = ones + 1

            # check positive diagonals for pattern _X__
            elif (
                board[r][c] == 0
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == 0
                and board[r + 3][c + 3] == 0
            ):
                ones = ones + 1

            # check positive diagonals for pattern __X_
            elif (
                board[r][c] == 0
                and board[r + 1][c + 1] == 0
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == 0
            ):
                ones = ones + 1

            # check negative diagonals for pattern _XXX
            if (
                board[r + 3][c] == 0
                and board[r + 2][c + 1] == piece
                and board[r + 1][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                if (r + 3) % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check negative diagonals for pattern X_XX
            elif (
                board[r + 3][c] == piece
                and board[r + 2][c + 1] == 0
                and board[r + 1][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                if (r + 2) % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check negative diagonals for pattern XX_X
            elif (
                board[r + 3][c] == piece
                and board[r + 2][c + 1] == piece
                and board[r + 1][c + 2] == 0
                and board[r][c + 3] == piece
            ):
                if (r + 1) % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check negative diagonals for pattern XXX_
            elif (
                board[r + 3][c] == piece
                and board[r + 2][c + 1] == piece
                and board[r + 1][c + 2] == piece
                and board[r][c + 3] == 0
            ):
                if r % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check negative diagonals for pattern __XX
            elif (
                board[r + 3][c] == 0
                and board[r + 2][c + 1] == 0
                and board[r + 1][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                twos = twos + 1

            # check negative diagonals for pattern X__X
            elif (
                board[r + 3][c] == piece
                and board[r + 2][c + 1] == 0
                and board[r + 1][c + 2] == 0
                and board[r][c + 3] == piece
            ):
                twos = twos + 1

            # check negative diagonals for pattern XX__
            elif (
                board[r + 3][c] == piece
                and board[r + 2][c + 1] == piece
                and board[r + 1][c + 2] == 0
                and board[r][c + 3] == 0
            ):
                twos = twos + 1

            # check negative diagonals for pattern _XX_
            elif (
                board[r + 3][c] == 0
                and board[r + 2][c + 1] == piece
                and board[r + 1][c + 2] == piece
                and board[r + 0][c + 3] == 0
            ):
                twos = twos + 1

            # check negative diagonals for pattern ___X
            elif (
                board[r + 3][c] == 0
                and board[r + 2][c + 1] == 0
                and board[r + 1][c + 2] == 0
                and board[r][c + 3] == piece
            ):
                ones = ones + 1

            # check negative diagonals for pattern X___
            elif (
                board[r + 3][c] == piece
                and board[r + 2][c + 1] == 0
                and board[r + 1][c + 2] == 0
                and board[r][c + 3] == 0
            ):
                ones = ones + 1

            # check negative diagonals for pattern _X__
            elif (
                board[r + 3][c] == 0
                and board[r + 2][c + 1] == piece
                and board[r + 1][c + 2] == 0
                and board[r][c + 3] == 0
            ):
                ones = ones + 1

            # check negative diagonals for pattern __X_
            elif (
                board[r + 3][c] == 0
                and board[r + 2][c + 1] == 0
                and board[r + 1][c + 2] == piece
                and board[r][c + 3] == 0
            ):
                ones = ones + 1

    for c in range(COLUMN_COUNT):

        for r in range(ROW_COUNT - 3):

            # check verticals for pattern _XXX
            if (
                board[r][c] == 0
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                if r % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check verticals for pattern X_XX
            elif (
                board[r][c] == piece
                and board[r + 1][c] == 0
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                if (r + 1) % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check verticals for pattern XX_X
            elif (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == 0
                and board[r + 3][c] == piece
            ):
                if (r + 2) % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check verticals for pattern XXX_
            elif (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == 0
            ):
                if (r + 3) % 2 == 0:
                    even_threes = even_threes + 1
                else:
                    odd_threes = odd_threes + 1

            # check verticals for pattern __XX
            elif (
                board[r][c] == 0
                and board[r + 1][c] == 0
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                twos = twos + 1

            # check verticals for pattern X__X
            elif (
                board[r][c] == piece
                and board[r + 1][c] == 0
                and board[r + 2][c] == 0
                and board[r + 3][c] == piece
            ):
                twos = twos + 1

            # check verticals for pattern XX__
            elif (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == 0
                and board[r + 3][c] == 0
            ):
                twos = twos + 1

            # check verticals for pattern _XX_
            elif (
                board[r][c] == 0
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == 0
            ):
                twos = twos + 1

            # check verticals for pattern ___X
            elif (
                board[r][c] == 0
                and board[r + 1][c] == 0
                and board[r + 2][c] == 0
                and board[r + 3][c] == piece
            ):
                ones = ones + 1

            # check verticals for pattern X___
            elif (
                board[r][c] == piece
                and board[r + 1][c] == 0
                and board[r + 2][c] == 0
                and board[r + 3][c] == piece
            ):
                ones = ones + 1

            # check verticals for pattern _X__
            elif (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == 0
                and board[r + 3][c] == 0
            ):
                ones = ones + 1

            # check verticals for pattern __X_
            elif (
                board[r][c] == 0
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == 0
            ):
                ones = ones + 1

    return even_threes, odd_threes, twos, ones


def score_columns(board, piece):
    score = 0
    for r in range(ROW_COUNT):
        # if in middle column
        middle = int((COLUMN_COUNT - 1) / 2)
        if board[r][middle] == piece:
            score = score + 200
        # if in surrounding two columns
        left = int(((COLUMN_COUNT - 1) / 2) - 1)
        right = int(((COLUMN_COUNT - 1) / 2) + 1)
        if board[r][left] == piece or board[r][right] == piece:
            score = score + 50
    return score


def get_score(board, depth):
    # offset ensures ai chooses quickest win
    offset = MINIMAX_DEPTH - depth
    if four_in_a_row(board, PLAYER_PIECE):
        return -1000000 + offset
    elif four_in_a_row(board, AI_PIECE):
        return 1000000 - offset
    else:
        score = 0
        player_even_threes, player_odd_threes, player_twos, player_ones = in_a_row(board, PLAYER_PIECE)
        ai_even_threes, ai_odd_threes, ai_twos, ai_ones = in_a_row(board, AI_PIECE)
        score = score - 2400 * player_even_threes
        score = score + 1800 * ai_even_threes
        score = score - 1800 * player_odd_threes
        score = score + 2400 * ai_odd_threes
        score = score - 300 * player_twos
        score = score + 300 * ai_twos
        score = score - 20 * player_ones
        score = score + 20 * ai_ones
        score = score - score_columns(board, PLAYER_PIECE)
        score = score + score_columns(board, AI_PIECE)
        return score


# minimax with alpha-beta pruning
def get_best_move(board, depth, alpha=float("-inf"), beta=float("inf"), isAI=True):

    if (
        depth == 0
        or four_in_a_row(board, PLAYER_PIECE)
        or four_in_a_row(board, AI_PIECE)
    ):
        score = get_score(board, depth)
        return None, score

    if isAI:
        bestScore = float("-inf")
        col = get_valid_locations(board)[0]
        # for loop iterates out from center, i.e. [3, 2, 4, 1, 5, 0, 6]
        for c in get_valid_locations(board):
            r = get_next_open_row(board, c)
            drop_piece(board, r, c, AI_PIECE)

            # recursive function call
            score = get_best_move(board, depth - 1, alpha, beta, False)[1]

            board[r][c] = 0
            if score > bestScore:
                bestScore = score
                col = c

            # alpha-beta pruning
            alpha = max(alpha, bestScore)
            if alpha >= beta:
                break

        return col, bestScore

    else:
        bestScore = float("inf")
        col = get_valid_locations(board)[0]
        # for loop iterates out from center, i.e. [3, 2, 4, 1, 5, 0, 6]
        for c in get_valid_locations(board):
            r = get_next_open_row(board, c)
            drop_piece(board, r, c, PLAYER_PIECE)

            # recursive function call
            score = get_best_move(board, depth - 1, alpha, beta, True)[1]

            board[r][c] = 0
            if score < bestScore:
                bestScore = score
                col = c

            # alpha-beta pruning
            beta = min(beta, bestScore)
            if alpha >= beta:
                break

        return col, bestScore
