import numpy as np
import cv2 as cv
import math
from connect4ai import *

CAMERA_ID = 1


# get yellow mask
def yellow_mask(board):
    lower = np.array([20, 50, 100])
    upper = np.array([30, 255, 255])
    return cv.inRange(board, lower, upper)


# get red mask
def red_mask(board):
    # lower = np.array([0, 50, 50])
    # upper = np.array([10, 255, 255])
    lower2 = np.array([170, 50, 50])
    upper2 = np.array([180, 255, 255])
    # mask = cv.inRange(board, lower, upper)
    mask2 = cv.inRange(board, lower2, upper2)
    return mask2  # mask + mask2


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
            cv.circle(blur, (i[0], i[1]), round(i[2] / 2), (0, 0, 255), 5)

    # hough tranform to find yellow circles
    ycirs = cv.HoughCircles(
        yellow_mask(hsv),
        cv.HOUGH_GRADIENT,
        2,
        75,
        param1=50,
        param2=30,
        minRadius=20,
        maxRadius=50,
    )
    if ycirs is not None:
        ycirs = np.uint16(np.around(ycirs))
        for i in ycirs[0, :]:
            # mark yellow circles
            cv.circle(blur, (i[0], i[1]), round(i[2] / 2), (0, 255, 255), 5)

    for i in range(1, ROW_COUNT):
        cv.line(
            blur,
            (0, round(blur.shape[0] * (float(i) / ROW_COUNT))),
            (blur.shape[1], round(blur.shape[0] * (float(i) / ROW_COUNT))),
            (255, 255, 255),
            thickness=2,
            lineType=8,
        )

    for i in range(1, COLUMN_COUNT):
        cv.line(
            blur,
            (round(blur.shape[1] * (float(i) / COLUMN_COUNT)), 0),
            (round(blur.shape[1] * (float(i) / COLUMN_COUNT)), blur.shape[0]),
            (255, 255, 255),
            thickness=2,
            lineType=8,
        )

    return blur, cirs, rcirs, ycirs


# check position in grid
def grid_pos(position, board):
    row = math.floor((position[1] / board.shape[0]) * ROW_COUNT)
    col = math.floor((position[0] / board.shape[1]) * COLUMN_COUNT)
    return row, col


# converts circle data to an workable array
def to_array(cirs, rcirs, ycirs, img):
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    for cir in cirs[0, :]:

        # detect red tokens
        if rcirs is not None:
            for rcir in rcirs[0, :]:
                if (
                    float(cir[0]) - float(cir[2])
                    < float(rcir[0])
                    < float(cir[0]) + float(cir[2])
                ) and (
                    float(cir[1]) - float(cir[2])
                    < float(rcir[1])
                    < float(cir[1]) + float(cir[2])
                ):
                    row, col = grid_pos(cir, img)
                    board[row][col] = 1

        # detect yellow tokens
        if ycirs is not None:
            for ycir in ycirs[0, :]:
                if (
                    float(cir[0]) - float(cir[2])
                    < float(ycir[0])
                    < float(cir[0]) + float(cir[2])
                ) and (
                    float(cir[1]) - float(cir[2])
                    < float(ycir[1])
                    < float(cir[1]) + float(cir[2])
                ):
                    row, col = grid_pos(cir, img)
                    board[row][col] = 2

    return board


def check_board(cirs, rcirs, ycirs, board):

    # get token counts
    if rcirs is not None:
        rcount = len(rcirs[0])
    else:
        rcount = 0
    if ycirs is not None:
        ycount = len(ycirs[0])
    else:
        ycount = 0

    # check token counts
    if (len(cirs[0]) != (ROW_COUNT * COLUMN_COUNT)) or (rcount - ycount != 1):
        return False

    # check board positions
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 1):
            if (
                board[r + 1][c] == PLAYER_PIECE or board[r + 1][c] == AI_PIECE
            ) and board[r][c] == 0:
                return False
    return True


def compare_boards(board1, board2):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if not board1[r][c] == board2[r][c]:
                return False
    return True


game_board = np.zeros((ROW_COUNT, COLUMN_COUNT))
prev_board = game_board
board_valid = False
# connect to camera
vid = cv.VideoCapture(CAMERA_ID)

while True:

    # waiting for other player's move
    while not board_valid or compare_boards(game_board, prev_board):

        ret, img = vid.read()
        # perform hough analysis
        final_img, circles, red_circles, yellow_circles = hough(img)
        # my webcam reads in the video upside down
        cv.imshow("detected circles", cv.rotate(final_img, cv.ROTATE_180))
        cv.waitKey(500)
        # get and check board
        game_board = to_array(circles, red_circles, yellow_circles, final_img)
        board_valid = check_board(circles, red_circles, yellow_circles, game_board)

    if four_in_a_row(game_board, PLAYER_PIECE) or four_in_a_row(game_board, AI_PIECE):
        break
    prev_board = game_board
    print(get_best_move(game_board, MINIMAX_DEPTH))

print("game won!")
vid.release()
cv.destroyAllWindows()
