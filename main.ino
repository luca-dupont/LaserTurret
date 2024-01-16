#include <Servo.h>

String serialData;

Servo serX;
Servo serY;

struct Pos {
  int x;
  int y;
};

void setup() {
  serX.attach(10);
  serY.attach(11);
  Serial.begin(9600); // Set the baud rate to match your Python script
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

Pos parsePos(String coords) {
  Pos pos = {0,0};
  int yIndex = coords.indexOf("Y");

  pos.x = coords.substring(1,yIndex).toInt();
  pos.y = coords.substring(yIndex+1).toInt();

  return pos;
}

