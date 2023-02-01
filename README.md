[![Connect 4 Robot](http://img.youtube.com/vi/lbCc1O47Izo/0.jpg)](http://www.youtube.com/watch?v=lbCc1O47Izo "Connect 4 Robot")
\
\
This is code I wrote to enable an arduino-based DIY robotic arm to play a human opponent in Connect 4. There are four parts:\
&nbsp;&nbsp;&nbsp;&nbsp;(1) connect4ai.py - runs analysis on the board state and determines the best move\
&nbsp;&nbsp;&nbsp;&nbsp;(2) connect4opencv.py - reads in a processable array from a video stream of the physical board\
&nbsp;&nbsp;&nbsp;&nbsp;(3) connect4robot.py - sets up connections and communicates with the arduino over bluetooth\
&nbsp;&nbsp;&nbsp;&nbsp;(4) connect4arduino.ino - recieves bluetooth signals and directs servo movements\
\
The ai is written using a minimax algorithm (starting at the middle column of the board and working outwards) with alpha-beta pruning. Each game board is scored based on wins, combinations of three pieces and an open space, combinations of two pieces and two open spaces, combinations of one piece and three open spaces, and controlling the center columns. The OpenCV computer vision code uses a hough circle algorithm to identify the board grid layout and red and yellow masks to determine the position of each piece.
