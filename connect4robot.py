import socket
from connect4ai import *
from connect4opencv import *

MINIMAX_DEPTH = 6

serverMACAddress = '98:d3:41:f5:ca:2a'
port = 1
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
while 1:
    text = input()
    if text == "quit":
        break
    s.send(bytes(text, 'UTF-8'))
s.close()

# default variables to get started
game_board = np.zeros((ROW_COUNT, COLUMN_COUNT))
prev_board = game_board
board_valid = False
diff = 1

# connect to camera
vid = cv.VideoCapture(CAMERA_ID)

while True:

    # waiting for other player's move
    # runs again if the board isn't valid or if the boards don't have a valid token diff
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

    # check for win
    if four_in_a_row(game_board, PLAYER_PIECE) or four_in_a_row(game_board, AI_PIECE):
        break

    prev_board = game_board
    diff = 2
    print(get_best_move(game_board, MINIMAX_DEPTH))

# finish
print("game won!")
vid.release()
cv.destroyAllWindows()