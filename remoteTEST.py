import pymysql
import RPi.GPIO as GPIO
import time
#db = pymysql.connect("localhost", "newuser1", "lab301", "newdb2")
#cursor = db.cursor()

# GPIO setup
GPIO.setmode(GPIO.BOARD)
pin = [11, 13, 15]
for i in pin:
    GPIO.setup(i, GPIO.OUT)


def S():
    GPIO.output(pin[0], GPIO.LOW)
    GPIO.output(pin[1], GPIO.LOW)
    GPIO.output(pin[2], GPIO.LOW)
    print("S")


def G():
    GPIO.output(pin[0], GPIO.HIGH)
    GPIO.output(pin[1], GPIO.LOW)
    GPIO.output(pin[2], GPIO.LOW)
    time.sleep(1)
    print("G")
    #S()


def B():
    GPIO.output(pin[0], GPIO.LOW)
    GPIO.output(pin[1], GPIO.HIGH)
    GPIO.output(pin[2], GPIO.LOW)
    time.sleep(1)
    print("B")


def L():
    GPIO.output(pin[0], GPIO.HIGH)
    GPIO.output(pin[1], GPIO.HIGH)
    GPIO.output(pin[2], GPIO.LOW)
    time.sleep(1)
    print("L")
    #S()


def R():
    GPIO.output(pin[0], GPIO.LOW)
    GPIO.output(pin[1], GPIO.LOW)
    GPIO.output(pin[2], GPIO.HIGH)
    time.sleep(1)
    print("R")
    #S()


def O():
    GPIO.output(pin[0], GPIO.HIGH)
    GPIO.output(pin[1], GPIO.LOW)
    GPIO.output(pin[2], GPIO.HIGH)
    time.sleep(1)
    print("O")
    #S()


def C():
    GPIO.output(pin[0], GPIO.LOW)
    GPIO.output(pin[1], GPIO.HIGH)
    GPIO.output(pin[2], GPIO.HIGH)
    time.sleep(1)
    print("C")
    #S()

while True:
    #cursor.execute("SELECT Direction, Clamp FROM remote")
    #row = cursor.fetchone()
    #db.commit()
    #print(row)
    intruction = input("Enter direction:")
    if intruction is not None:
        print(intruction)
        
        if(intruction == "S"):
            S()
        elif(intruction == "G"):
            G()
        elif(intruction == "B"):
            B()
        elif(intruction == "L"):
            L()
        elif(intruction == "R"):
            R()
        if(intruction == "O"):
            O()
        elif(intruction == "C"):
            C()
        
    time.sleep(0.2)
            