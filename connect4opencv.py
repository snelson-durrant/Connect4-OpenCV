import sys
import numpy as np
import cv2 as cv

# generate yellow mask
def yellow_mask(board):
    lower = np.array([20, 100, 100])
    upper = np.array([30, 255, 255])
    return cv.inRange(board, lower, upper)


# generate red mask
def red_mask(board):
    lower = np.array([0, 50, 50])
    upper = np.array([10, 255, 255])
    lower2 = np.array([170, 50, 50])
    upper2 = np.array([180, 255, 255])
    mask = cv.inRange(board, lower, upper)
    mask2 = cv.inRange(board, lower2, upper2)
    return mask + mask2


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
        cv.circle(blurred, (i[0], i[1]), round(i[2] / 2), (0, 255, 255), 2)

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
        cv.circle(blurred, (i[0], i[1]), round(i[2] / 2), (0, 0, 255), 2)

# display results
cv.imshow("detected circles", blurred)
cv.waitKey(0)
cv.destroyAllWindows()

for circle in circles[0, :]:
    for red_circle in red_circles[0, :]:
        if (
            circle[0] - circle[2] / 2 < red_circle[0] < circle[0] + circle[2] / 2
        ) and (
            circle[1] - circle[2] / 2 < red_circle[1] < circle[1] + circle[2] / 2
        ):
            print("red hit!")
    for yellow_circle in yellow_circles[0, :]:
        if (
            circle[0] - circle[2] / 2 < yellow_circle[0] < circle[0] + circle[2] / 2
        ) and (
            circle[1] - circle[2] / 2 < yellow_circle[1] < circle[1] + circle[2] / 2
        ):
            print("yellow hit!")
