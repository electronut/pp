/* 

lissajous.ino

Most of this code is from the following source:

Controlling 2 motors with the TB6612FNG + Arduino 

http://bildr.org/2012/04/tb6612fng-arduino/

The only changes I have made are in the loops, where I am reading motor data from the serial port.

-- Mahesh Venkitachalam

*/

//motor A connected between A01 and A02
//motor B connected between B01 and B02

int STBY = 10; //standby

//Motor A
int PWMA = 3; //Speed control 
int AIN1 = 9; //Direction
int AIN2 = 8; //Direction

//Motor B
int PWMB = 5; //Speed control
int BIN1 = 11; //Direction
int BIN2 = 12; //Direction

void setup(){
  pinMode(STBY, OUTPUT);

  pinMode(PWMA, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);

  pinMode(PWMB, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);

  // initialize the serial communication:
  Serial.begin(9600);
}

// Mahesh Venkitachalam:
// main loop that reads motor data sent by laser.py 
void loop() {
		 
  // The data sent is of the form:
  // 'H' (header), speed1, dir1, speed2, dir2
  if (Serial.available() >= 5) {
    if(Serial.read() == 'H') {
      // read the most recent byte (which w  ill be from 0 to 255):
      byte s1 = Serial.read();
      byte d1 = Serial.read();
      byte s2 = Serial.read();
      byte d2 = Serial.read();
      
      // stop motor if both speeds are 0
      if(s1 == 0 && s2 == 0) {
        stop();
      }
      else {
        move(0, s1, d1);
        move(1, s2, d2);
      }
      delay(20);
    }
    else {
      // invalid data, stop motors
      stop(); 
    }
  }
  else {
    // no data 
    delay(250);
  }
}

// Mahesh Venkitachalam:
// This method just ramps motor speeds up and down - useful for testing setup
// rename this to loop() for testing
void loop3() {
 
  for(int i = 0; i < 255; i+=8) {
    
    move(1, i, 1);

    for(int j = 0; j < 255; j+=8) {
      move(2, j, 1);
      delay(20);
    }
  }  
  
  stop();
  delay(250);
  
  for(int i = 0; i < 255; i+=8) {
  
    move(1, i, 2);

    for(int j = 0; j < 255; j+=8) {
      move(2, j, 1);
      delay(20);
    }
  }  
  
  stop();
  delay(250);
}

void loop2(){
  move(1, 255, 1); //motor 1, full speed, left
  move(2, 255, 1); //motor 2, full speed, left

  delay(1000); //go for 1 second
  stop(); //stop
  delay(250); //hold for 250ms until move again

  move(1, 128, 0); //motor 1, half speed, right
  move(2, 128, 0); //motor 2, half speed, right

  delay(1000);
  stop();
  delay(250);
}

void move(int motor, int speed, int direction){
//Move specific motor at speed and direction
//motor: 0 for B 1 for A
//speed: 0 is off, and 255 is full speed
//direction: 0 clockwise, 1 counter-clockwise

  digitalWrite(STBY, HIGH); //disable standby

  boolean inPin1 = LOW;
  boolean inPin2 = HIGH;

  if(direction == 1){
    inPin1 = HIGH;
    inPin2 = LOW;
  }

  if(motor == 1){
    digitalWrite(AIN1, inPin1);
    digitalWrite(AIN2, inPin2);
    analogWrite(PWMA, speed);
  }else{
    digitalWrite(BIN1, inPin1);
    digitalWrite(BIN2, inPin2);
    analogWrite(PWMB, speed);
  }
}

void stop(){
//enable standby  
  digitalWrite(STBY, LOW);
}
