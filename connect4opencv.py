import sys
import numpy as np
import cv2 as cv
import math

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
    row = math.floor(position[0] / (board.shape[0] / 6))  # ROW_COUNT
    col = math.floor(position[1] / (board.shape[1] / 7))  # COLUMN_COUNT
    return row, col


# get board state
def read_board(cirs, rcirs, ycirs):
    board = np.zeros((6, 7))

    for cir in cirs[0, :]:
        for rcir in rcirs[0, :]:
            if (cir[0] - cir[2] / 2 < rcir[0] < cir[0] + cir[2] / 2) and (
                cir[1] - cir[2] / 2 < rcir[1] < cir[1] + cir[2] / 2
            ):
                row, col = check_grid(rcir, blurred)
                board[col][row] = 1

        for ycir in ycirs[0, :]:
            if (cir[0] - cir[2] / 2 < ycir[0] < cir[0] + cir[2] / 2) and (
                cir[1] - cir[2] / 2 < ycir[1] < cir[1] + cir[2] / 2
            ):
                row, col = check_grid(ycir, blurred)
                board[col][row] = 2

    return np.flip(board)


# read in the file
img = cv.imread(sys.argv[1], 1)

# standardize image size and blur
desired_width = 800
aspect_ratio = desired_width / img.shape[1]
desired_height = int(img.shape[0] * aspect_ratio)
dim = (desired_width, desired_height)
resized = cv.resize(img, dsize=dim, interpolation=cv.INTER_AREA)
blurred = cv.medianBlur(resized, 5)

# get image types
hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)

# hough transform on all circles
circles = cv.HoughCircles(
    gray, cv.HOUGH_GRADIENT, 1, 75, param1=50, param2=30, minRadius=20, maxRadius=50
)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv.circle(blurred, (i[0], i[1]), i[2], (255, 0, 0), 2)
        cv.circle(blurred, (i[0], i[1]), 2, (0, 0, 0), 3)

# hough tranform on red circles
red_circles = cv.HoughCircles(
    red_mask(hsv),
    cv.HOUGH_GRADIENT,
    2,
    75,
    param1=50,
    param2=30,
    minRadius=20,
    maxRadius=50,
)
if red_circles is not None:
    red_circles = np.uint16(np.around(red_circles))
    for i in red_circles[0, :]:
        cv.circle(blurred, (i[0], i[1]), round(i[2] / 2), (0, 255, 255), 4)

# hough tranform on yellow circles
yellow_circles = cv.HoughCircles(
    yellow_mask(hsv),
    cv.HOUGH_GRADIENT,
    2,
    75,
    param1=50,
    param2=30,
    minRadius=1,
    maxRadius=50,
)
if yellow_circles is not None:
    yellow_circles = np.uint16(np.around(yellow_circles))
    for i in yellow_circles[0, :]:
        cv.circle(blurred, (i[0], i[1]), round(i[2] / 2), (0, 0, 255), 4)

# display results
cv.imshow("detected circles", blurred)
cv.waitKey(0)
cv.destroyAllWindows()

print(read_board(circles, red_circles, yellow_circles))
