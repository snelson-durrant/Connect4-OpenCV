Check out a video of the working project here: https://www.youtube.com/watch?v=lbCc1O47Izo
\
\
This repository contains code I wrote for a custom-built robotic arm capable of playing a human opponent in Connect 4. There are four parts:\
&nbsp;&nbsp;&nbsp;&nbsp;(1) connect4ai.py - *runs analysis on the current board state and determines the next move*\
&nbsp;&nbsp;&nbsp;&nbsp;(2) connect4opencv.py - *converts the video stream into a processable board state representation*\
&nbsp;&nbsp;&nbsp;&nbsp;(3) connect4robot.py - *sets up connections and communicates with the microcontroller over bluetooth*\
&nbsp;&nbsp;&nbsp;&nbsp;(4) connect4arduino.ino - *recieves bluetooth commands and directs servo movements*\
\
The move decision component is written using a minimax algorithm (starting at the middle column of the board and working outwards) with alpha-beta pruning. Each game board is scored based on wins, combinations of three pieces and an open space, combinations of two pieces and two open spaces, combinations of one piece and three open spaces, and controlling the center columns. The OpenCV computer vision code uses a hough circle algorithm to identify the board grid layout and red and yellow color masks to determine the position of each respective piece.
