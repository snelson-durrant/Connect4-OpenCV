import sys
import numpy as np
import cv2 as cv
import math
from connect4ai import *


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


# check position in grid
def grid_pos(position, board):
    row = math.floor(position[0] / (board.shape[0] / ROW_COUNT))
    col = math.floor(position[1] / (board.shape[1] / COLUMN_COUNT))
    return row, col


# converts circle data to an workable array
def to_array(cirs, rcirs, ycirs, img):
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))

    for cir in cirs[0, :]:
        # detect red tokens
        for rcir in rcirs[0, :]:
            if (cir[0] - cir[2] / 2 < rcir[0] < cir[0] + cir[2] / 2) and (
                cir[1] - cir[2] / 2 < rcir[1] < cir[1] + cir[2] / 2
            ):
                row, col = grid_pos(rcir, img)
                board[col][row] = 1
        # detect yellow tokens
        for ycir in ycirs[0, :]:
            if (cir[0] - cir[2] / 2 < ycir[0] < cir[0] + cir[2] / 2) and (
                cir[1] - cir[2] / 2 < ycir[1] < cir[1] + cir[2] / 2
            ):
                row, col = grid_pos(ycir, img)
                board[col][row] = 2

    return np.flip(board)


# VIDEO WARPER FUNCTION
# qr codes on board itself?


def count_tokens(board):
    player = 0
    ai = 0
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                player += 1
            if board[r][c] == AI_PIECE:
                ai += 1
    return player, ai


def check_board(board):
    valid = True
    player, ai = count_tokens(board)
    if player - ai > 1 or ai - player > 1:
        valid = False
    for c in range(COLUMN_COUNT - 1):
        for r in range(ROW_COUNT - 1):
            if (
                board[r + 1][c] == PLAYER_PIECE or board[r + 1][c] == AI_PIECE
            ) and board[r][c] == 0:
                valid = False
    return valid


# WRITE IN FROM VIDEO, UPDATING EVERY TWO SECONDS OR SO
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
print(check_board(game_board))
