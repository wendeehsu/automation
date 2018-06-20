#include <Servo.h>
#include <Ultrasonic.h>

Servo myservo;  // create servo object to control a servo
Ultrasonic ultrasonicR(12,13);
Ultrasonic ultrasonicL(10,11);

int servoRIGHT =5;
int servoLEFT = 9;
int Full = 10;
int Medium = 60;
int Slow = 80;
int VerySlow = 100;
bool R = false;
bool L = false;
String str;
int distanceL;
int distanceR;

void servoControlRIGHT(bool R){
  if (R == true)
  {
    digitalWrite(servoRIGHT, HIGH);
    delayMicroseconds(1000);  //move front
    digitalWrite(servoRIGHT, LOW);
  }
  if (R == false)
  {
    digitalWrite(servoRIGHT, HIGH);
    delayMicroseconds(2000); //move back
    digitalWrite(servoRIGHT, LOW);
  }
  
}
void servoControlLEFT(bool L){
  if (L == true){
    digitalWrite(servoLEFT, HIGH);
    delayMicroseconds(2000);
    digitalWrite(servoLEFT, LOW);
  }
  if (L == false){
    digitalWrite(servoLEFT, HIGH);
    delayMicroseconds(1000);
    digitalWrite(servoLEFT, LOW);
  }
}

void pause(){
  digitalWrite(servoLEFT, HIGH);
  digitalWrite(servoRIGHT, HIGH);
  delayMicroseconds(1500);
  digitalWrite(servoLEFT, LOW);
  digitalWrite(servoRIGHT, LOW);
}

void move(bool R, bool L){
  for(int i=0; i<10;i++){
    servoControlRIGHT(R);
    servoControlLEFT(L);
    delay(10);
  }
}

void setup() {
    Serial.begin(9600);
    myservo.attach(3);  // attaches the servo on pin 3 to the servo object
    myservo.write(90);
    pinMode(servoRIGHT, OUTPUT);
    pinMode(servoLEFT, OUTPUT);
    digitalWrite(servoRIGHT, HIGH);
    digitalWrite(servoLEFT, HIGH);
    delayMicroseconds(1500);
    digitalWrite(servoRIGHT, LOW);
    digitalWrite(servoLEFT, LOW);
    delay(20);
}

int cases = 1; //1: looking for ball, 2: facing obstacles
void loop() {
  if(cases == 1){
    if (Serial.available() > 0){
      int s = Serial.read();
      Serial.println(s);

      //clamp
      if(s == 79){  //"O" = CLOSE
        myservo.write(180);
        Serial.println("CLOSE");
        cases = 2;
      }
      else if(s == 67){ //"C" = open 
        myservo.write(90);  //OPEN
        Serial.println("OPEN");
      }

      //moving direction
      else if(s == 76){ //"L"
        Serial.println("turn left");
        L = false;
        R = true;
        move(R, L);        
      }
      else if(s == 82){ //"R"
        Serial.println("turn right");
        L = true;
        R = false;
        move(R, L);
      }
      else if(s == 71){ //"G"
        Serial.println("move front");
        L = true;
        R = true;
        move(R, L);
      }
      else if(s == 83){ //"S"
        Serial.println("stop");
        pause();
        L = false;
        R = false;
      } 
    }
  }
  else if(cases == 2){
    distanceL = ultrasonicL.distanceRead();
    distanceR = ultrasonicR.distanceRead();
    Serial.print("Distance in CM: ");
    Serial.print(distanceL);
    Serial.print(" ");
    Serial.println(distanceR);
  
    if ((distanceL-distanceR) > 15){
      Serial.print("L\n");
      R = true;
      L = false;
    }
    else if ((distanceR-distanceL) > 15){
      Serial.print("R\n");
      R = false;
      L = true;
    }
    else if (distanceL < 15 && distanceR < 15){
      Serial.print("B\n");
      R = false;
      L = false;
    }
    else{
      Serial.print("F\n");
      R = true;
      L = true;
    }
    move(R, L);
  }
}

