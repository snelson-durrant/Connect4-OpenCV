// #include <Arduino.h>
#include <SoftwareSerial.h>
#include <Servo.h>

Servo servo01;
Servo servo02;
Servo servo03;
Servo servo04;

SoftwareSerial Bluetooth(0, 1);

int servo1Pos, servo2Pos, servo3Pos, servo4Pos;
int servo1PPos, servo2PPos, servo3PPos, servo4PPos;
int speedDelay = 20;
int index = 0;
String dataIn = "";
bool isReset = true;

int moveServo(Servo servo, int &pos, int &ppos)
{

  if (ppos > pos)
  {
    for (int i = ppos; i >= pos; i--)
    {
      servo.write(i);
      delay(speedDelay);
    }
  }

  if (ppos < pos)
  {
    for (int i = ppos; i <= pos; i++)
    {
      servo.write(i);
      delay(speedDelay);
    }
  }

  ppos = pos;
  return 0;
}

void setup()
{
  // initialize servos and bluetooth
  servo01.attach(2);
  servo02.attach(3);
  servo03.attach(4);
  servo04.attach(5);
  Bluetooth.begin(9600);
  Bluetooth.setTimeout(1);
  delay(20);

  // initial position
  servo1PPos = 90;
  servo01.write(servo1PPos);
  servo2PPos = 100;
  servo02.write(servo2PPos);
  servo3PPos = 110;
  servo03.write(servo3PPos);
  servo4PPos = 120;
  servo04.write(servo4PPos);
}

void loop()
{
  // Check for incoming data
  if (Bluetooth.available() > 0)
  {
    dataIn = Bluetooth.readString();
  }

  if (dataIn == "0")
  {

    servo1Pos = 0;
    moveServo(servo01, servo1Pos, servo1PPos);
    servo2Pos = 0;
    moveServo(servo02, servo2Pos, servo2PPos);
    servo3Pos = 0;
    moveServo(servo03, servo3Pos, servo3PPos);
    servo4Pos = 0;
    moveServo(servo04, servo4Pos, servo4PPos);
    isReset = false;
  }
  else if (dataIn == "1")
  {

    servo1Pos = 20;
    moveServo(servo01, servo1Pos, servo1PPos);
    servo2Pos = 20;
    moveServo(servo02, servo2Pos, servo2PPos);
    servo3Pos = 20;
    moveServo(servo03, servo3Pos, servo3PPos);
    servo4Pos = 20;
    moveServo(servo04, servo4Pos, servo4PPos);
    isReset = false;
  }
  else if (dataIn == "2")
  {

    servo1Pos = 40;
    moveServo(servo01, servo1Pos, servo1PPos);
    servo2Pos = 40;
    moveServo(servo02, servo2Pos, servo2PPos);
    servo3Pos = 40;
    moveServo(servo03, servo3Pos, servo3PPos);
    servo4Pos = 40;
    moveServo(servo04, servo4Pos, servo4PPos);
    isReset = false;
  }
  else if (dataIn == "3")
  {

    servo1Pos = 60;
    moveServo(servo01, servo1Pos, servo1PPos);
    servo2Pos = 60;
    moveServo(servo02, servo2Pos, servo2PPos);
    servo3Pos = 60;
    moveServo(servo03, servo3Pos, servo3PPos);
    servo4Pos = 60;
    moveServo(servo04, servo4Pos, servo4PPos);
    isReset = false;
  }
  else if (dataIn == "4")
  {

    servo1Pos = 80;
    moveServo(servo01, servo1Pos, servo1PPos);
    servo2Pos = 80;
    moveServo(servo02, servo2Pos, servo2PPos);
    servo3Pos = 80;
    moveServo(servo03, servo3Pos, servo3PPos);
    servo4Pos = 80;
    moveServo(servo04, servo4Pos, servo4PPos);
    isReset = false;
  }
  else if (dataIn == "5")
  {

    servo1Pos = 100;
    moveServo(servo01, servo1Pos, servo1PPos);
    servo2Pos = 100;
    moveServo(servo02, servo2Pos, servo2PPos);
    servo3Pos = 100;
    moveServo(servo03, servo3Pos, servo3PPos);
    servo4Pos = 100;
    moveServo(servo04, servo4Pos, servo4PPos);
    isReset = false;
  }
  else if (dataIn == "6")
  {

    servo1Pos = 120;
    moveServo(servo01, servo1Pos, servo1PPos);
    servo2Pos = 120;
    moveServo(servo02, servo2Pos, servo2PPos);
    servo3Pos = 120;
    moveServo(servo03, servo3Pos, servo3PPos);
    servo4Pos = 120;
    moveServo(servo04, servo4Pos, servo4PPos);
    isReset = false;
  }
  else
  {

    // reset position
    if (not isReset)
    {
      servo1Pos = 180;
      moveServo(servo01, servo1Pos, servo1PPos);
      servo2Pos = 180;
      moveServo(servo02, servo2Pos, servo2PPos);
      servo3Pos = 180;
      moveServo(servo03, servo3Pos, servo3PPos);
      servo4Pos = 180;
      moveServo(servo04, servo4Pos, servo4PPos);
      isReset = true;
    }
  }
}
