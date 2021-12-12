import cv2
from collections import deque
import numpy as np
import keyboard
import pygame

##################
# Functions #
##################


def nothing(x):
    global trackbarSelected
    trackbarSelected = True


def getCentroidFromContour(contour):
    M = cv2.moments(c)
    centroid = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    return centroid


def euclidean(pt1, pt2):
    d = np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
    return round(d, 2)


def drawThresholdAndText(frame, frame_size, thresh_upper, thresh_lower,
                         thresh_left, thresh_right):
    # draw threshold lines in frame
    lineColor = (0, 0, 255)
    cv2.line(frame, (0, thresh_upper), (frame_size[1], thresh_upper),
             lineColor, 1)  # upper line
    cv2.line(frame, (0, thresh_lower), (frame_size[1], thresh_lower),
             lineColor, 1)  # lower thresh
    cv2.line(frame, (thresh_left, 0), (thresh_left, frame_size[0]), lineColor,
             1)  # left line
    cv2.line(frame, (thresh_right, 0), (thresh_right, frame_size[0]),
             lineColor, 1)  # right line

    # draw text
    cv2.putText(frame, 'Jump', (thresh_left + 20, thresh_upper - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)

    cv2.putText(frame, 'Duck', (thresh_left + 20, thresh_lower + 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)

    cv2.putText(frame, 'Fire', (thresh_right + 10, thresh_lower - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)


def drawTailOnFrame(pointTail, bufferSize, frame):
    for i in range(1, len(pointTail)):
        # if either of the tracked points are None, ignore them
        if pointTail[i - 1] is None or pointTail[i] is None:
            continue
        # otherwise, draw tail as line segments by computing the thickness of each line segments
        thickness = int(np.sqrt(bufferSize / float(i + 1)) * 2.5)
        cv2.line(frame, pointTail[i - 1], pointTail[i], (0, 0, 255), thickness)


# check 1 times per 3 frame and press the keyboard by the location of the point
# def pressKeyboard(point, check_cnt, check_every, last_event, up, down, left,right):
def pressKeyboard(point, check_cnt, check_every, last_event):
    if point is not None:
        # print(point, check_cnt)
        if check_cnt >= check_every:
            if point is not None:
                if point[1] < thresh_upper:
                    last_event = "jump"
                elif point[1] > thresh_lower:
                    last_event = "duck"
                elif point[0] > thresh_right:
                    last_event = "fire"
                elif point[0] < 25:
                    last_event = "cheat"
                else:
                    if last_event == "jump" or "duck" or "fire" or "cheat":
                        last_event = None
            check_cnt = 0

    if check_cnt == 0:
        if last_event == "jump":
            keyboard.press("up")
            # up.play()
        elif last_event == "duck":
            keyboard.press("down")
            # down.play()
        elif last_event == "fire":
            keyboard.press("space")
            # right.play()
        # enable cheat mode if object is at the right side of the screen
        elif last_event == "cheat": 
            keyboard.press("delete")
            keyboard.release("delete")
            print("--------------CHEAT MODE SWITCH---------------")
        else:
            keyboard.release("down")
            keyboard.release("up")
            keyboard.release("space")
        # print(point[0], point[1], last_event)
    check_cnt += 1

    return check_cnt, last_event


# transform the black part of the image to white
def black2white(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 10, cv2.THRESH_BINARY)
    img[thresh == 0] = 255
    return img


##########################################################################################

##################
# Set parameters #
##################
frame_size = (180, 320)  # camera size (180, 320) 9:16

cheatStatus = False

# variables for keyboard control
last_event = None
check_every = 3  # check mark position every three avalable frames
check_cnt = 0  # current check count
minColorRadius = 15  # only detect color with minEnclosingCircle bigger than 'minColorRadius'

# define boundaries of the color to find in HSV
colorLower = None
colorUpper = None
bufferSize = 2  # Set buffersize for the tail (list of tracked points)
trackbarSelected = False

##################
# Initializations #
##################
# initialize the tail (list of tracked points)
pointTail = deque(maxlen=bufferSize)
# initiliza selected color Color Palette
colorPalette = np.zeros((40, frame_size[1], 3), np.uint8)

# initialze pygame and read in sound files
pygame.mixer.init()
# sound = pygame.mixer.Sound('./sounds/beep.mp3')
# left = pygame.mixer.Sound('./sounds/left_fast.mp3')
# right = pygame.mixer.Sound('./sounds/right_fast.mp3')
# up = pygame.mixer.Sound('./sounds/up_fast.mp3')
# down = pygame.mixer.Sound('./sounds/down_fast.mp3')

# set up a window for color calibration
cv2.namedWindow("Color Calibration")
cv2.createTrackbar("BLUE", "Color Calibration", 255, 255, nothing)
cv2.createTrackbar("GREEN", "Color Calibration", 180, 255, nothing)
cv2.createTrackbar("RED", "Color Calibration", 0, 255, nothing)

cam = cv2.VideoCapture(0)

#I------|--------------------------|------
#N      |                          |
#C------|--------thresh_upper------|------
#R      |                          |
#E      |                          |
#S------|-------thresh_lower-------|------
#E      |                          |
#⬇️-----|--------------------------|-------
thresh_lower = int(frame_size[0] * 0.6)
thresh_upper = int(frame_size[0] * 0.4)
thresh_left = int(frame_size[1] * 0.3)
thresh_right = int(frame_size[1] * 0.7)

while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        print("ERROR: No camera frame.")
        break

    # set color threshold using GUI
    B = cv2.getTrackbarPos("BLUE", "Color Calibration")
    G = cv2.getTrackbarPos("GREEN", "Color Calibration")
    R = cv2.getTrackbarPos("RED", "Color Calibration")
    colorPalette[:] = [B, G, R]
    rgbColorSelected = np.uint8([[[B, G, R]]])
    hsvColorSelected = cv2.cvtColor(rgbColorSelected, cv2.COLOR_BGR2HSV)
    colorLower = np.uint8([hsvColorSelected[0][0][0] - 10, 100, 100])
    colorUpper = np.uint8([hsvColorSelected[0][0][0] + 10, 255, 255])

    # Camera frame manipulation
    frame = cv2.flip(frame, 1)  # flipped around y axis
    frame = cv2.resize(frame, (frame_size[1], frame_size[0]))
    # blur the frame, and convert it to the HSV color space
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # construct a mask for the color to find
    # perform dilations and erosions to remove any small blobs
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    maskedFrame = cv2.bitwise_and(frame, frame, mask=mask)

    # draw threshold lines and correspoding text
    drawThresholdAndText(frame, frame_size, thresh_upper, thresh_lower,
                         thresh_left, thresh_right)
    drawThresholdAndText(mask, frame_size, thresh_upper, thresh_lower,
                         thresh_left, thresh_right)

    # find contours in the mask and initialize the centroid of the color to find
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    centroid = None
    mark = None  # is the position used to judge keyboard action. Could be centerOfEnclosingCircle

    # draw text to color pallet todo
    if trackbarSelected:
        cv2.putText(colorPalette, 'COLOR SELECTED',
                    (int(frame_size[0] / 2), 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    else:
        cv2.putText(colorPalette, 'PLEASE SELECT COLOR', (int(frame_size[0] / 2) - 20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # only proceed if at least one contour was found
    if len(contours) > 0:
        # find the largest contour in the mask
        c = max(contours, key=cv2.contourArea)
        # compute the minimum enclosing circle and its center
        (mark, radius) = cv2.minEnclosingCircle(c)
        mark = (int(mark[0]), int(mark[1]))

        # print("Radius of color: " + str(radius))

        # only proceed if the radius meets a minimum size
        if radius > minColorRadius:
            # # get and draw centroid
            # centroid = getCentroidFromContour(c)
            # cv2.circle(frame, centroid, 5, (0, 0, 255), -1)

            # draw the circle on the frame
            cv2.circle(frame, mark, int(radius), (0, 255, 255),
                       2)  # draw enclosing circle

            # update the list of tracked points (tail)
            pointTail.appendleft(mark)

            # draw tail
            drawTailOnFrame(pointTail, bufferSize, frame)
            drawTailOnFrame(pointTail, bufferSize, maskedFrame)

            # press key board according to mark position
            # check_cnt, last_event = pressKeyboard(mark, check_cnt, check_every,last_event, up, down, left,                                          right)
            check_cnt, last_event = pressKeyboard(mark, check_cnt, check_every,
                                                  last_event)
                                                  

    # show images in windows
    # cv2.imshow("Color inRange mask", mask) # for debug
    # cv2.imshow("Camera", frame)
    # cv2.imshow("Masked Frame", maskedFrame)
    maskedFrame = black2white(maskedFrame)
    concatImages = np.concatenate((colorPalette, maskedFrame, frame), axis=0)
    cv2.imshow("Color Calibration", concatImages)

    # Press Q to quit
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
