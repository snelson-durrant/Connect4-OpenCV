import socket
import time
from connect4ai import *
from connect4opencv import *
from playsound import playsound
import threading

HC05_ADDRESS = "98:d3:41:f5:ca:2a"
PORT = 1

# default variables to get started
game_board = np.zeros((ROW_COUNT, COLUMN_COUNT))
prev_board = game_board
board_valid = False
diff = 1
champion = False

# connect to Arduino bluetooth module
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((HC05_ADDRESS, PORT))
print("BLUETOOTH CONNECTION SUCCESSFUL!")

# connect to camera
vid = cv.VideoCapture(CAMERA_ID)
print("CAMERA CONNECTION SUCCESSFUL!")


def playmusic():
    playsound("C:/Users/snels/Music/champions.mp3")


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
    s.send(str(7).encode())
    robot_move, move_score = get_best_move(game_board, MINIMAX_DEPTH)
    print_board(game_board)
    print("move selection: " + str(robot_move))
    print("move score: " + str(move_score))
    time.sleep(2)
    s.send(str(robot_move).encode())
    print("SENT TO ROBOT!")

    # check to see if a win is inevitable
    # if so, play "We Are The Champions" like a living legend
    if (move_score > 900000) and not champion:
        music = threading.Thread(target=playmusic, args=(), daemon=True)
        print("WE ARE THE CHAMPIONS!")
        music.start()
        champion = True

    # check move_score for ai win
    if move_score == 999999:
        break

    # reset loop
    prev_board = game_board
    diff = 2

# finish
print()
print("GAME OVER!")
time.sleep(2)
vid.release()
cv.destroyAllWindows()

input("press any key to exit")
s.close()
