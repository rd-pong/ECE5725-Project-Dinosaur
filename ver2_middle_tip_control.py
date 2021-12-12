# RUN 'python ver2_middle_tip_control.py'

import mediapipe as mp
import cv2
import numpy as np
import keyboard
import pygame

pygame.mixer.init()
# sound = pygame.mixer.Sound('sounds/beep.mp3')
# left = pygame.mixer.Sound('sounds/left_fast.mp3')
# right = pygame.mixer.Sound('sounds/right_fast.mp3')
# up = pygame.mixer.Sound('sounds/up_fast.mp3')
# down = pygame.mixer.Sound('sounds/down_fast.mp3')

cam = cv2.VideoCapture(0)
frame_size = (180, 320)

last_event = None
check_cnt = 0
check_every = 3

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#I###############################
#N#
#C#########thresh_upper###########
#R#
#E#
#S#########thresh_lower##########
#E#
#⬇️#############################
thresh_lower = int(frame_size[0] * 0.65)
thresh_upper = int(frame_size[0] * 0.35)
thresh_left = int(frame_size[1] * 0.3)
thresh_right = int(frame_size[1] * 0.7)


def euclidean(pt1, pt2):
    d = np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
    return round(d, 2)


with mp_hands.Hands(static_image_mode=True,
                    max_num_hands=1,
                    min_detection_confidence=0.6) as hands:
    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (frame_size[1], frame_size[0]))

        h, w, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False

        res = hands.process(rgb)
        rgb.flags.writeable = True

        # draw thresh
        cv2.line(frame, (0, thresh_upper), (frame_size[1], thresh_upper),
                 (0, 255, 0), 1)  # upper line
        cv2.line(frame, (0, thresh_lower), (frame_size[1], thresh_lower),
                 (0, 255, 0), 1)  # lower thresh
        cv2.line(frame, (thresh_left, 0), (thresh_left, frame_size[0]),
                 (0, 255, 0), 1)  # left line
        cv2.line(frame, (thresh_right, 0), (thresh_right, frame_size[0]),
                 (0, 255, 0), 1)  # right line

        # draw text
        cv2.putText(frame, 'Jump', (thresh_left+20,thresh_upper-30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 1, cv2.LINE_AA)

        cv2.putText(frame, 'Duck', (thresh_left+20,thresh_lower+50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 1, cv2.LINE_AA)

        cv2.putText(frame, 'Fire', (thresh_right+10,thresh_lower-15), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 1, cv2.LINE_AA)

        if res.multi_hand_landmarks:
            for hand_landmarks in res.multi_hand_landmarks:

                mark = mp_drawing._normalized_to_pixel_coordinates(  # middle_tip
                    hand_landmarks.landmark[
                        mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x,
                    hand_landmarks.landmark[
                        mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y, w, h)

                if mark is not None:
                    # print(mark, check_cnt)
                    if check_cnt >= check_every:
                        if mark is not None:
                            if mark[1] < thresh_upper:
                                last_event = "jump"
                            elif mark[1] > thresh_lower:
                                last_event = "duck"
                            elif mark[0] > thresh_right:
                                last_event = "fire"
                            else:
                                if last_event == "jump" or "duck" or "fire":
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
                    else:
                        keyboard.release("down")
                        keyboard.release("up")
                        keyboard.release("space")
                    # print(mark[0], mark[1], last_event)
                    print(last_event)
                check_cnt += 1

                # mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS) # draw hand using mediapipe
                cv2.circle(frame, mark, 5, (0, 0, 255), -1)

        cv2.imshow("Controller Window", frame)

        if cv2.waitKey(1) & 0xFF == 2:
            break
cam.release()
cv2.destroyAllWindows()
