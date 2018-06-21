# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import pymysql
import time
import RPi.GPIO as GPIO

# Read db
db = pymysql.connect("localhost", "newuser1", "lab301", "newdb2")
cursor = db.cursor()
row = []

read = True
while read:
    time.sleep(1)  #wait for 1 second
    cursor.execute("SELECT color, id FROM Client_info WHERE color != 0")
    row = cursor.fetchone()
    if row is not None:
        read = False
        print(row[0], row[1])

id_color = {1: "red", 2: "yellow", 3: "green", 4: "purple", 5: "blue"}
ball_color = {1: "red", 2: "yellow", 3: "green", 4: "blue", 5: "purple"}

a = ball_color[row[0]]
b = id_color[row[1]]

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
    S()


def B():
    GPIO.output(pin[0], GPIO.LOW)
    GPIO.output(pin[1], GPIO.HIGH)
    GPIO.output(pin[2], GPIO.LOW)
    time.sleep(1)
    print("B")
    S()


def L():
    GPIO.output(pin[0], GPIO.HIGH)
    GPIO.output(pin[1], GPIO.HIGH)
    GPIO.output(pin[2], GPIO.LOW)
    time.sleep(1)
    print("L")
    S()


def R():
    GPIO.output(pin[0], GPIO.LOW)
    GPIO.output(pin[1], GPIO.LOW)
    GPIO.output(pin[2], GPIO.HIGH)
    time.sleep(1)
    print("R")
    S()


def O():
    GPIO.output(pin[0], GPIO.HIGH)
    GPIO.output(pin[1], GPIO.LOW)
    GPIO.output(pin[2], GPIO.HIGH)
    time.sleep(1)
    print("O")
    S()


def C():
    GPIO.output(pin[0], GPIO.LOW)
    GPIO.output(pin[1], GPIO.HIGH)
    GPIO.output(pin[2], GPIO.HIGH)
    time.sleep(1)
    print("C")
    S()


class color:
    def __init__(self, lower, upper):
        self.upper = upper
        self.lower = lower


#define the colors' upper and lower bound
Red = color((170, 50, 50), (210, 255, 255))
Yellow = color((10, 50, 100), (30, 255, 255))
Green = color((50, 50, 130), (90, 255, 255))
Blue = color((90, 100, 100), (130, 255, 255))
Purple = color((150, 40, 60), (170, 255, 180))
colorArray = {
    'red': Red,
    'yellow': Yellow,
    'green': Green,
    'blue': Blue,
    'purple': Purple
}

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# ball in the HSV color space, then initialize the list of tracked points
#get the intended color

a, b = input("Enter : Color of ball and paper\n").split(" ")

pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    #Current case-> 0: catch ball 1:ball arrival
    case = 0
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorArray[a].lower, colorArray[a].upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in np.arange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        #cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show the frame to our screen
    cv2.imshow("Frame", frame)

    # Find the position of ball in the view of camera
    # the x position of catching ball is 269~309
    # the y position of catching ball is 360
    Gotcha_pos_left = 240  # x pos
    Gotcha_pos_right = 400  # x pos
    Gotcha_near = 360  # y pos
    view_width = 480
    view_length = 640
    # Check the x axis of center of ball if it is near the right side
    if center is None:
        R()
    elif center[0] > Gotcha_pos_right:
        R()
    # Check if it is near left side
    elif center[0] < Gotcha_pos_left:
        L()
    elif center[0] >= Gotcha_pos_left and center[0] <= Gotcha_pos_right:
        G()
        if center[1] >= Gotcha_near:
            G()
            G()
            G()
            O()
            a = b
            print("Near the target!!")
            if case == 1:
                B()
                B()
                cursor.execute(
                    "UPDATE Client_info SET color = 0,send_status = 0 WHERE send_status =1"
                )
            case += 1

    key = cv2.waitKey(1) & 0xFF
    if center is not None:
        print("Center: {}, Radius: {}".format(center, radius))
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()