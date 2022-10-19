// #include <Arduino.h>
#include <Servo.h>

Servo servo01;
Servo servo02;
Servo servo03;
Servo servo04;
Servo servo05;
Servo servo06;

int servo1Pos, servo2Pos, servo3Pos, servo4Pos, servo5Pos, servo6Pos;
int servo1PPos, servo2PPos, servo3PPos, servo4PPos, servo5PPos, servo6PPos;
int speedDelay = 20;
String dataIn = "";

// move servo at a designated speed
int moveServo(Servo servo, int& pos, int& ppos) {

  if (ppos > pos) {
    for ( int i = ppos; i >= pos; i--) {
      servo.write(i);
      delay(speedDelay);
    }
  }

  if (ppos < pos) {
    for ( int i = ppos; i <= pos; i++) {
      servo.write(i);
      delay(speedDelay);
    }
  }

  ppos = pos;
  return 0;
}

void setup() {
  
  // initialize servos and bluetooth
  servo01.attach(2);
  servo02.attach(3);
  servo03.attach(4);
  servo04.attach(5);
  servo05.attach(6);
  servo06.attach(7);
  Serial.begin(9600);
  delay(20);

  // initial position
  servo1PPos = 90;
  servo01.write(servo1PPos);
  servo2PPos = 70;
  servo02.write(servo2PPos);
  servo3PPos = 90;
  servo03.write(servo3PPos);
  servo4PPos = 120;
  servo04.write(servo4PPos);
  servo5PPos = 150;
  servo05.write(servo5PPos);
  servo6PPos = 80;
  servo06.write(servo6PPos);
  
}

void loop() {
  
  // check for incoming data
  if (Serial.available() > 0) {
    dataIn = Serial.readString();
    Serial.print(dataIn);

    // pick up a piece
    servo1Pos = 1;
    moveServo(servo01, servo1Pos, servo1PPos);
    delay(50);

    // reset robot arm position
    servo1Pos = 90;
    moveServo(servo01, servo1Pos, servo1PPos);
    servo2Pos = 90;
    moveServo(servo02, servo2Pos, servo2PPos);
    servo3Pos = 90;
    moveServo(servo03, servo3Pos, servo3PPos);
    servo4Pos = 120;
    moveServo(servo04, servo4Pos, servo4PPos);
    servo5Pos = 150;
    moveServo(servo05, servo5Pos, servo5PPos);
    servo6Pos = 70;
    moveServo(servo06, servo6Pos, servo6PPos);

    // check the bluetooth data for column selection
    if (dataIn == "0") {
  
      servo1Pos = 90;
      moveServo(servo01, servo1Pos, servo1PPos);
      servo2Pos = 90;
      moveServo(servo02, servo2Pos, servo2PPos);
      servo3Pos = 90;
      moveServo(servo03, servo3Pos, servo3PPos);
      servo4Pos = 120;
      moveServo(servo04, servo4Pos, servo4PPos);
      servo5Pos = 150;
      moveServo(servo05, servo5Pos, servo5PPos);
      servo6Pos = 70;
      moveServo(servo06, servo6Pos, servo6PPos);
  
    } else if (dataIn == "1") {
  
      servo1Pos = 90;
      moveServo(servo01, servo1Pos, servo1PPos);
      servo2Pos = 90;
      moveServo(servo02, servo2Pos, servo2PPos);
      servo3Pos = 90;
      moveServo(servo03, servo3Pos, servo3PPos);
      servo4Pos = 120;
      moveServo(servo04, servo4Pos, servo4PPos);
      servo5Pos = 150;
      moveServo(servo05, servo5Pos, servo5PPos);
      servo6Pos = 80;
      moveServo(servo06, servo6Pos, servo6PPos);
  
    } else if (dataIn == "2") {
  
      servo5Pos = 120;
      moveServo(servo05, servo5Pos, servo5PPos);
      delay(50);
      servo1Pos = 90;
      moveServo(servo01, servo1Pos, servo1PPos);
  
    } else if (dataIn == "3") {
  
      servo1Pos = 90;
      moveServo(servo01, servo1Pos, servo1PPos);
      servo2Pos = 90;
      moveServo(servo02, servo2Pos, servo2PPos);
      servo3Pos = 90;
      moveServo(servo03, servo3Pos, servo3PPos);
      servo4Pos = 120;
      moveServo(servo04, servo4Pos, servo4PPos);
      servo5Pos = 150;
      moveServo(servo05, servo5Pos, servo5PPos);
      servo6Pos = 80;
      moveServo(servo06, servo6Pos, servo6PPos);
  
    } else if (dataIn == "4") {
  
      servo1Pos = 90;
      moveServo(servo01, servo1Pos, servo1PPos);
      servo2Pos = 90;
      moveServo(servo02, servo2Pos, servo2PPos);
      servo3Pos = 90;
      moveServo(servo03, servo3Pos, servo3PPos);
      servo4Pos = 120;
      moveServo(servo04, servo4Pos, servo4PPos);
      servo5Pos = 150;
      moveServo(servo05, servo5Pos, servo5PPos);
      servo6Pos = 80;
      moveServo(servo06, servo6Pos, servo6PPos);

    } else if (dataIn == "5") {
  
      servo1Pos = 90;
      moveServo(servo01, servo1Pos, servo1PPos);
      servo2Pos = 90;
      moveServo(servo02, servo2Pos, servo2PPos);
      servo3Pos = 90;
      moveServo(servo03, servo3Pos, servo3PPos);
      servo4Pos = 120;
      moveServo(servo04, servo4Pos, servo4PPos);
      servo5Pos = 150;
      moveServo(servo05, servo5Pos, servo5PPos);
      servo6Pos = 80;
      moveServo(servo06, servo6Pos, servo6PPos);
  
    } else if (dataIn == "6") {
  
      servo1Pos = 90;
      moveServo(servo01, servo1Pos, servo1PPos);
      servo2Pos = 90;
      moveServo(servo02, servo2Pos, servo2PPos);
      servo3Pos = 90;
      moveServo(servo03, servo3Pos, servo3PPos);
      servo4Pos = 120;
      moveServo(servo04, servo4Pos, servo4PPos);
      servo5Pos = 150;
      moveServo(servo05, servo5Pos, servo5PPos);
      servo6Pos = 80;
      moveServo(servo06, servo6Pos, servo6PPos);
  
    }

    // reset robot arm position
    servo1Pos = 90;
    moveServo(servo01, servo1Pos, servo1PPos);
    servo2Pos = 90;
    moveServo(servo02, servo2Pos, servo2PPos);
    servo3Pos = 90;
    moveServo(servo03, servo3Pos, servo3PPos);
    servo4Pos = 120;
    moveServo(servo04, servo4Pos, servo4PPos);
    servo5Pos = 150;
    moveServo(servo05, servo5Pos, servo5PPos);
    servo6Pos = 70;
    moveServo(servo06, servo6Pos, servo6PPos);
    
  }
}
