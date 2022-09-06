import sys
import numpy as np
import cv2 as cv
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER_PIECE = 1
AI_PIECE = 2

MINIMAX_DEPTH = 6


def sort_from_middle(list, reverse=False):
    if len(list) <= 1:
        return list
    tail = sorted([list[-1], list[0]], reverse=reverse)
    return sort_from_middle(list[1:-1], reverse) + tail


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


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

    # check horizontals for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # check verticals for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # check positive diagonals for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # check negative diagonals for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True


def three_in_a_row(board, piece):
    locations = []

    # check horizontals for pattern _XXX
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == 0
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                locations.append([r, c])

    # check verticals for pattern _XXX
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == 0
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                locations.append([r, c])

    # check positive diagonals for pattern _XXX
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == 0
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                locations.append([r, c])

    # check negative diagonals for pattern _XXX
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == 0
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                locations.append([r, c])

    # check horizontals for pattern X_XX
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == 0
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                locations.append([r, c + 1])

    # check verticals for pattern X_XX
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == 0
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                locations.append([r + 1, c])

    # check positive diagonals for pattern X_XX
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == 0
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                locations.append([r + 1, c + 1])

    # check negative diagonals for pattern X_XX
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == 0
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                locations.append([r - 1, c + 1])

    # check horizontals for pattern XX_X
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == 0
                and board[r][c + 3] == piece
            ):
                locations.append([r, c + 2])

    # check verticals for pattern XX_X
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == 0
                and board[r + 3][c] == piece
            ):
                locations.append([r + 2, c])

    # check positive diagonals for pattern XX_X
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == 0
                and board[r + 3][c + 3] == piece
            ):
                locations.append([r + 2, c + 2])

    # check negative diagonals for pattern XX_X
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == 0
                and board[r - 3][c + 3] == piece
            ):
                locations.append([r - 2, c + 2])

    # check horizontals for pattern XXX_
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == 0
            ):
                locations.append([r, c + 3])

    # check verticals for pattern XXX_
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == 0
            ):
                locations.append([r + 3, c])

    # check positive diagonals for pattern XXX_
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == 0
            ):
                locations.append([r + 3, c + 3])

    # check negative diagonals for pattern XXX_
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == 0
            ):
                locations.append([r - 3, c + 3])

    return locations


def two_in_a_row(board, piece):
    locations = []

    # check horizontals for pattern _XX
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == 0
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
            ):
                locations.append([r, c])

    # check verticals for pattern _XX
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 2):
            if (
                board[r][c] == 0
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
            ):
                locations.append([r, c])

    # check positive diagonals for pattern _XX
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT - 2):
            if (
                board[r][c] == 0
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
            ):
                locations.append([r, c])

    # check negative diagonals for pattern _XX
    for c in range(COLUMN_COUNT - 2):
        for r in range(2, ROW_COUNT):
            if (
                board[r][c] == 0
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
            ):
                locations.append([r, c])

    # check horizontals for pattern X_X
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == 0
                and board[r][c + 2] == piece
            ):
                locations.append([r, c + 1])

    # check verticals for pattern X_X
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 2):
            if (
                board[r][c] == piece
                and board[r + 1][c] == 0
                and board[r + 2][c] == piece
            ):
                locations.append([r + 1, c])

    # check positive diagonals for pattern X_X
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT - 2):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == 0
                and board[r + 2][c + 2] == piece
            ):
                locations.append([r + 1, c + 1])

    # check negative diagonals for pattern X_X
    for c in range(COLUMN_COUNT - 2):
        for r in range(2, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == 0
                and board[r - 2][c + 2] == piece
            ):
                locations.append([r - 1, c + 1])

    # check horizontals for pattern XX_
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == 0
            ):
                locations.append([r, c + 2])

    # check verticals for pattern XX_
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 2):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == 0
            ):
                locations.append([r + 2, c])

    # check positive diagonals for pattern XX_
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT - 2):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == 0
            ):
                locations.append([r + 2, c + 2])

    # check negative diagonals for pattern XX_
    for c in range(COLUMN_COUNT - 2):
        for r in range(2, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == 0
            ):
                locations.append([r - 2, c + 2])

    return locations


def one_in_a_row(board, piece):
    locations = []

    # check horizontals for pattern _X
    for c in range(COLUMN_COUNT - 1):
        for r in range(ROW_COUNT):
            if board[r][c] == 0 and board[r][c + 1] == piece:
                locations.append([r, c])

    # check verticals for pattern _X
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 1):
            if board[r][c] == 0 and board[r + 1][c] == piece:
                locations.append([r, c])

    # check positive diagonals for pattern _X
    for c in range(COLUMN_COUNT - 1):
        for r in range(ROW_COUNT - 1):
            if board[r][c] == 0 and board[r + 1][c + 1] == piece:
                locations.append([r, c])

    # check negative diagonals for pattern _X
    for c in range(COLUMN_COUNT - 1):
        for r in range(1, ROW_COUNT):
            if board[r][c] == 0 and board[r - 1][c + 1] == piece:
                locations.append([r, c])

    # check horizontals for pattern X_
    for c in range(COLUMN_COUNT - 1):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == 0:
                locations.append([r, c + 1])

    # check verticals for pattern X_
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 1):
            if board[r][c] == piece and board[r + 1][c] == 0:
                locations.append([r + 1, c])

    # check positive diagonals for pattern X_
    for c in range(COLUMN_COUNT - 1):
        for r in range(ROW_COUNT - 1):
            if board[r][c] == piece and board[r + 1][c + 1] == 0:
                locations.append([r + 1, c + 1])

    # check negative diagonals for pattern X_
    for c in range(COLUMN_COUNT - 1):
        for r in range(1, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == 0:
                locations.append([r - 1, c + 1])

    return locations


def score_columns(board, piece):
    score = 0
    validLocations = get_valid_locations(board)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # if in middle column
            if board[r][c] == piece and c == validLocations[0]:
                score = score + 30
            # if in surrounding two columns
            elif board[r][c] == piece and (validLocations[1] or c == validLocations[2]):
                score = score + 10
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
        for three in three_in_a_row(board, PLAYER_PIECE):
            score = score - 900
        for three in three_in_a_row(board, AI_PIECE):
            score = score + 900
        for two in two_in_a_row(board, PLAYER_PIECE):
            score = score - 300
        for two in two_in_a_row(board, AI_PIECE):
            score = score + 300
        for one in one_in_a_row(board, PLAYER_PIECE):
            score = score - 20
        for one in one_in_a_row(board, AI_PIECE):
            score = score + 20
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


# get yellow mask
def yellow_mask(board):
    lower = np.array([20, 100, 100])
    upper = np.array([30, 255, 255])
    return cv.inRange(board, lower, upper)


# get red mask
def red_mask(board):
    lower = np.array([0, 50, 50])
    upper = np.array([10, 255, 255])
    lower2 = np.array([170, 50, 50])
    upper2 = np.array([180, 255, 255])
    mask = cv.inRange(board, lower, upper)
    mask2 = cv.inRange(board, lower2, upper2)
    return mask + mask2


# check position in grid
def check_grid(position, board):
    row = math.floor(position[0] / (board.shape[0] / ROW_COUNT))  # ROW_COUNT
    col = math.floor(position[1] / (board.shape[1] / COLUMN_COUNT))  # COLUMN_COUNT
    return row, col


# converts circle data to an workable array
def to_array(cirs, rcirs, ycirs, img):
    board = np.zeros((ROW_COUNT, COLUMN_COUNT)) # ROW AND COLUMN COUNT

    for cir in cirs[0, :]:
        # detect red tokens
        for rcir in rcirs[0, :]:
            if (cir[0] - cir[2] / 2 < rcir[0] < cir[0] + cir[2] / 2) and (
                cir[1] - cir[2] / 2 < rcir[1] < cir[1] + cir[2] / 2
            ):
                row, col = check_grid(rcir, img)
                board[col][row] = 1
        # detect yellow tokens
        for ycir in ycirs[0, :]:
            if (cir[0] - cir[2] / 2 < ycir[0] < cir[0] + cir[2] / 2) and (
                cir[1] - cir[2] / 2 < ycir[1] < cir[1] + cir[2] / 2
            ):
                row, col = check_grid(ycir, img)
                board[col][row] = 2

    return np.flip(board)


# image preprocessing
def preprocess(img):

    # standardize image size and blur
    desired_width = 800
    aspect_ratio = desired_width / img.shape[1]
    desired_height = int(img.shape[0] * aspect_ratio)
    dim = (desired_width, desired_height)
    resized = cv.resize(img, dsize=dim, interpolation=cv.INTER_AREA)
    blur = cv.medianBlur(resized, 5)

    # get image types
    hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

    return blur, hsv, gray


# performs hough transforms
def hough(img):
    blur, hsv, gray = preprocess(img)

    # hough transform to find all circles
    cirs = cv.HoughCircles(
        gray, cv.HOUGH_GRADIENT, 1, 75, param1=50, param2=30, minRadius=20, maxRadius=50
    )
    if cirs is not None:
        cirs = np.uint16(np.around(cirs))
        for i in cirs[0, :]:
            # mark all circles
            cv.circle(blur, (i[0], i[1]), i[2], (255, 0, 0), 2)
            cv.circle(blur, (i[0], i[1]), 2, (0, 0, 0), 3)

    # hough tranform to find red circles
    rcirs = cv.HoughCircles(
        red_mask(hsv),
        cv.HOUGH_GRADIENT,
        2,
        75,
        param1=50,
        param2=30,
        minRadius=20,
        maxRadius=50,
    )
    if rcirs is not None:
        rcirs = np.uint16(np.around(rcirs))
        for i in rcirs[0, :]:
            # mark red circles
            cv.circle(blur, (i[0], i[1]), round(i[2] / 2), (0, 255, 255), 4)

    # hough tranform to find yellow circles
    ycirs = cv.HoughCircles(
        yellow_mask(hsv),
        cv.HOUGH_GRADIENT,
        2,
        75,
        param1=50,
        param2=30,
        minRadius=1,
        maxRadius=50,
    )
    if ycirs is not None:
        ycirs = np.uint16(np.around(ycirs))
        for i in ycirs[0, :]:
            # mark yellow circles
            cv.circle(blur, (i[0], i[1]), round(i[2] / 2), (0, 0, 255), 4)

    return blur, cirs, rcirs, ycirs


# read in the file
img = cv.imread(sys.argv[1], 1)

final_img, circles, red_circles, yellow_circles = hough(img)

# display results
cv.imshow("detected circles", final_img)
cv.waitKey(0)
cv.destroyAllWindows()

# finale
game_board = to_array(circles, red_circles, yellow_circles, final_img)
print(get_best_move(game_board, MINIMAX_DEPTH))
