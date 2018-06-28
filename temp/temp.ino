#include <Ultrasonic.h>
#include <Servo.h>

Servo myservo;  // create servo object to control a servo
Ultrasonic ultrasonicR(12,13);
Ultrasonic ultrasonicL(10,11);

int servoRIGHT =5;
int servoLEFT = 9;
bool R = false;
bool L = false;
int distanceL;
int distanceR;

void servoControlRIGHT(bool R){
  if (R == true)
  {
    digitalWrite(servoRIGHT, HIGH);
    delayMicroseconds(1000);  //move front
    digitalWrite(servoRIGHT, LOW);
  }
  else{
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
  else{
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
  delay(200);
}

void move(bool R, bool L,int t){
  for(int i=0; i<t;i++){
    servoControlRIGHT(R);
    servoControlLEFT(L);
    delay(50);
  }
}

bool ultraControl(int t1){
    distanceL = ultrasonicL.Ranging(CM);
    distanceR = ultrasonicR.Ranging(CM);

    Serial.print("Left distance = ");
    Serial.print(distanceL);
    Serial.print("Right distance = ");
    Serial.println(distanceR);

    int d = 8;
    if (distanceL< 2*d || distanceR < d){
        Serial.print("L\n");
        Serial.print(distanceL-distanceR);
        R = true;
        L = false;
        move(R, L, t1);
        return true;
    }
    else if (distanceL < d || distanceR < 2*d){
        Serial.print("R\n");
        R = false;
        L = true;
        move(R, L, t1);
        return true;
    }
    else if (distanceL < d && distanceR < d){
        Serial.print("B\n");
        R = false;
        L = false;
        move(R, L, t1);
        move(true,false,t1);
        return true;
    }else{
        return false;
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

int cases = 3; //1: looking for ball, 2: facing obstacles, 3: remote control
bool clampOpen = true;
void loop(){
    int a0 = digitalRead(A0);
    int a1 = digitalRead(A1);
    int a2 = digitalRead(A2);

    int t = 10;
    int t1 = 30;
    
    //clamp
    if(a0 == 0 && a1 == 1 && a2 == 1){  // CLOSE
        myservo.write(180);
        Serial.println("CLOSE");
        cases = 2;
        clampOpen = false;
    }
    else if(a0 == 1 && a1 == 0 && a2 == 1){ //open 
        if(!clampOpen || cases == 3){
            myservo.write(90);  //OPEN
            Serial.println("OPEN");
        }       
    }

    //moving direction
    if(a0 == 1 && a1 == 1 && a2 == 0){ //"L"
        Serial.println("turn left");
        L = false;
        R = true;
        if(cases == 2 && ultraControl(t1)){
            ;
        }else{
<<<<<<< HEAD
            move(R, L, t-5);        
=======
            move(R, L, t-5);
            if(cases != 3){
                delay(2000);        
            }
>>>>>>> 22ea8b15b319c98468d135107ac5f18c0b58c33a
        }
    }
    else if(a0 == 0 && a1 == 0 && a2 == 1){ //"R"
        Serial.println("turn right");
        L = true;
        R = false;
        if(cases == 2 && ultraControl(t1)){
            ;
        }else{
<<<<<<< HEAD
            move(R, L, t-5);        
=======
            move(R, L, t-5);  
            if(cases != 3){
                delay(2000);        
            }      
>>>>>>> 22ea8b15b319c98468d135107ac5f18c0b58c33a
        }
    }
    else if(a0 == 1 && a1 == 0 && a2 == 0){ //"G"
        Serial.println("move front");
        L = true;
        R = true;
        if(cases == 2 && ultraControl(t1)){
            ;
        }else{
            move(R, L, t);        
        }
    }
    else if(a0 == 0 && a1 == 1 && a2 == 0){ //"B"
        Serial.println("move BACK");
        L = false;
        R = false;
        move(R, L, t);        
    }
    else if(a0 == 0 && a1 == 0 && a2 == 0){ //"S"
        Serial.println("stop");
        pause();
    }
}
