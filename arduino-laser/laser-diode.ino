/* 

laser-diode.ino

Controlling two motors with an Arduino and 
Sparkfun Motor Driver 1A Dual TB6612FNG

A laser diode is attached to Pin 2 in this version, and is switched 
on/off by the code.

Reference:

http://bildr.org/2012/04/tb6612fng-arduino/

Author: Mahesh Venkitachalam
Website: electronut.in

*/

// motor #1 connected to A01 and A02
// motor #2 connected to B01 and B02

int STBY = 10; //standby

// Motor #1
int PWMA = 3; //Speed control 
int AIN1 = 9; //Direction
int AIN2 = 8; //Direction

// Motor #2
int PWMB = 5; //Speed control
int BIN1 = 11; //Direction
int BIN2 = 12; //Direction

// laser diode
int pinLaser = 2;

void setup(){

  pinMode(STBY, OUTPUT);

  pinMode(PWMA, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);

  pinMode(PWMB, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);

  pinMode(pinLaser, OUTPUT);
  
  // initialize the serial communication:
  Serial.begin(9600);
}

// main loop that reads motor data sent by laser.py 
void loop() 
{		 
  // The data sent is of the form:
  // 'H' (header), speed1, dir1, speed2, dir2
  if (Serial.available() >= 5) {
    
    // turn on laser
    digitalWrite(pinLaser, HIGH);
      
    if(Serial.read() == 'H') {
      // read next 4 bytes
      byte s1 = Serial.read();
      byte d1 = Serial.read();
      byte s2 = Serial.read();
      byte d2 = Serial.read();
      
      // stop motor if both speeds are 0
      if(s1 == 0 && s2 == 0) {
        stop();
      }
      else {
        // set speed and direction of both motors
        move(0, s1, d1);
        move(1, s2, d2);
      }
      // small pause
      delay(20);
    }
    else {
      // invalid data, stop motors
      stop(); 
      // turn off laser
      digitalWrite(pinLaser, LOW);
    }
  }
  else {
    // no data 
    delay(250);
    // turn off laser
    digitalWrite(pinLaser, LOW);
  }
}

// set motor speed and direction
// motor: #1 -> 1, #2 -> 0
// direction: 1/0 
void move(int motor, int speed, int direction)
{

  // disable standby
  digitalWrite(STBY, HIGH); 

  boolean inPin1 = LOW;
  boolean inPin2 = HIGH;

  if(direction == 1) {
    inPin1 = HIGH;
    inPin2 = LOW;
  }        
  
  if(motor == 1){
    digitalWrite(AIN1, inPin1);
    digitalWrite(AIN2, inPin2);
    analogWrite(PWMA, speed);
  }
  else{
    digitalWrite(BIN1, inPin1);
    digitalWrite(BIN2, inPin2);
    analogWrite(PWMB, speed);
  }
}

// bring motors to a stop
void stop(){
  // enable standby  
  digitalWrite(STBY, LOW);
}
