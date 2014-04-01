// ldr.ino
// 
// Read analog values from A0 and A1 and print them to serial port.
//
// Author: Mahesh Venkitachalam
// Website: electronut.in

#include "Arduino.h"

void setup()
{
  // initialize serial comms
  Serial.begin(9600); 
}

void loop()
{
  // read A0
  int val1 = analogRead(0);
  // read A1
  int val2 = analogRead(1);
  // print to serial
  Serial.print(val1);
  Serial.print(" ");
  Serial.print(val2);
  Serial.print("\n");
  // wait 
  delay(50);
}