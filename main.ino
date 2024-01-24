#include <Servo.h>

String serialData;

Servo serX;
Servo serY;

struct Pos {
  int x;
  int y;
};

void setup() {
  serX.attach(10); // pin 10 for X axis
  serY.attach(11); // pin 11 for Y axis
  Serial.begin(9600); // Set baud rate same as controller and FaceRec files
  Serial.setTimeout(10);
}

void loop() {
  // pass
}

void serialEvent() {
  serialData = Serial.readString();

  Pos coords = parsePos(serialData);

  serX.write(coords.x);
  serY.write(coords.y);
}

Pos parsePos(String coords) { // Parse data sent by controller or faceRec files
  Pos pos = {0,0};
  int yIndex = coords.indexOf("Y");

  pos.x = coords.substring(1,yIndex).toInt();
  pos.y = coords.substring(yIndex+1).toInt();

  return pos;
}

