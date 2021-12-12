# Map piTFT buttons to keyboard presses

import time
import RPi.GPIO as GPIO
import sys
import keyboard

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...
# setup piTFT buttons
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 17, 22, 3=23, 27 are piTFT buttons
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# def gpio17_callback(channel):   #  callback for gpio17 
#     print ("hit button 17")     #   set code_run with NO global

# def gpio22_callback(channel):   #  callback for gpio 22
#     global last_event
#     global curr_event
#     print ("hit button 22")     #   set var_a with NO global
#     # last_event = curr_event
#     curr_event = "jump"
#     # if last_event == "jump":
#     #     curr = None
        
# def gpio23_callback(channel):   #  callback for gpio 23
#     global last_event
#     global curr_event
#     print ("hit button 23")     #   set var_a with  global
#     # last_event = curr_event
#     curr_event = "duck"
#     # if last_event == "duck":
#     #     curr_event = None

# def gpio27_callback(channel):   #  callback for gpio 27
#     global code_run             # Set code_run with global
#     print ("quit")   # quit

# GPIO.add_event_detect(17, GPIO.FALLING, callback=gpio17_callback, bouncetime=400)
# GPIO.add_event_detect(27, GPIO.FALLING, callback=gpio27_callback, bouncetime=400)
# GPIO.add_event_detect(22, GPIO.FALLING, callback=gpio22_callback, bouncetime=400)
# GPIO.add_event_detect(23, GPIO.FALLING, callback=gpio23_callback, bouncetime=400)

code_run = True
last_event = None
curr_event = None

while code_run:
    # # Use Call back function
    # Working partially because we need a status rather than a event to 
    # trigger action control
    # print(last_event, curr_event)
    # if curr_event == "jump":
    #     keyboard.press("up")
    # elif curr_event == "duck":
    #     keyboard.press("down")
    # elif curr_event == "fire":
    #     keyboard.press("space")
    # else:
    #     keyboard.release("down")
    #     keyboard.release("up")
    #     keyboard.release("space")
    # # print(last_event)
    # last_event = curr_event
    # curr_event = None
    
    # Use GPIO status instead of callback function
    time.sleep(0.1)

    if GPIO.input(22) == 0:
        last_event = "jump"
    elif GPIO.input(22) == 1:
        last_event = None
    
    if last_event == None: 
        if GPIO.input(17) == 0:
            last_event = "fire"
        elif GPIO.input(17) == 1:
            last_event = None

    if last_event == None: 
        if GPIO.input(23) == 0:
            last_event = "duck"
        elif GPIO.input(23) == 1:
            last_event = None

    if last_event == "jump":
        keyboard.press("up")
    elif last_event == "duck":
        keyboard.press("down")
    elif last_event == "fire":
        keyboard.press("space")
    else:
        keyboard.release("down")
        keyboard.release("up")
        keyboard.release("space")
    # print(GPIO.input(22), GPIO.input(23) , last_event)

GPIO.cleanup()
