# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import pymysql
import time
import serial
<<<<<<< HEAD
ser = serial.Serial('/dev/ttyUSB1', 9600)
=======
ser = serial.Serial('/dev/myserial', 9600)
>>>>>>> 79eec9581a6ac014c64a0f16cdcade950b4901b4


class color:
    def __init__(self, lower, upper):
        self.upper = upper
        self.lower = lower


#define the colors' upper and lower bound
Red = color((170, 50, 50), (210, 255, 255))
Yellow = color((10, 50, 100), (30, 255, 255))
Green = color((50, 10, 70), (70, 255, 255))
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
a = input()
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
        continue
    elif center[0] > Gotcha_pos_right:
        ser.write("R".encode('utf-8'))
        print("R")
    # Check if it is near left side
    elif center[0] < Gotcha_pos_left:
        ser.write("L".encode('utf-8'))
        print("L")
        
    elif center[0] >= Gotcha_pos_left and center[0] <= Gotcha_pos_right:
        ser.write("G".encode('utf-8'))
        print("G")
        if center[1] >= Gotcha_near:
            ser.write("G".encode('utf-8'))
            print("G")
            ser.write("G".encode('utf-8'))
            print("G")
            ser.write("O".encode('utf-8'))
            print("O")
            break
        
    key = cv2.waitKey(1) & 0xFF
    if center is not None:
        print("Center: {}, Radius: {}".format(center, radius))
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

print("Terminated")
ser.write("S".encode('utf-8'))

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()