import socket
from connect4ai import *
from connect4opencv import *

serverMACAddress = "98:d3:41:f5:ca:2a"
port = 1

# default variables to get started
game_board = np.zeros((ROW_COUNT, COLUMN_COUNT))
prev_board = game_board
board_valid = False
diff = 1

# connect to Arduino bluetooth module
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress, port))
print("BLUETOOTH CONNECTION SUCCESSFUL!")

# connect to camera
vid = cv.VideoCapture(CAMERA_ID)
print("CAMERA CONNECTION SUCCESSFUL!")

while True:

    # waiting for player move
    # runs again if the board isn't valid or if the boards aren't different enough
    while not board_valid or same_boards(game_board, prev_board, diff):

        # perform hough analysis
        ret, img = vid.read()
        final_img, circles, red_circles, yellow_circles = hough(img)
        # note - my webcam reads in the video upside down
        cv.imshow("detected circles", cv.rotate(final_img, cv.ROTATE_180))
        cv.waitKey(500)
        # convert to array and check board
        game_board = to_array(circles, red_circles, yellow_circles, final_img)
        board_valid = check_board(circles, red_circles, yellow_circles, game_board)

    # check board for player win
    if four_in_a_row(game_board, PLAYER_PIECE):
        break

    # send move to robot
    robot_move, move_score = get_best_move(game_board, MINIMAX_DEPTH)
    print_board(game_board)
    print("move selection: " + str(robot_move))
    print("move score: " + str(move_score))
    s.send(bytes(robot_move))
    print("SENT TO ROBOT!")

    # TODO TEST THIS
    # check move_score for AI win
    if move_score == 1000:
        break

    # reset loop
    prev_board = game_board
    diff = 2

# finish
print("game over!")
vid.release()
cv.destroyAllWindows()
s.close()
