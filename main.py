import cv2
from datetime import date, datetime
import numpy as np
from logging import *
print('Imported libraries successfully.')

# Global Constants

HAAR_DATA = cv2.CascadeClassifier('data/frontfacedata.xml')
DEBUG = True
FONT = cv2.FONT_HERSHEY_SIMPLEX
VID = cv2.VideoCapture(0)


def find_face() -> list:

    ret, frame = VID.read()

    if ret:
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_coordinates = HAAR_DATA.detectMultiScale(grayscale)

        if len(face_coordinates) == 4:
            x, y, w, h = (each for each in face_coordinates)
            face_mask = [x, y, x + w, y + h]
            return face_mask

        if DEBUG:
            cv2.imshow('Raw Input', frame)
            cv2.imshow('Grayscale', grayscale)
            cv2.waitKey(1)
            print(face_coordinates)


def check_blink():
    pass


def check_yawn():
    pass


def facial_landmarks():
    pass


def exit_sequence() -> None:
    cv2.destroyAllWindows()
    text_log(message='Quit',
             curr_time=datetime.now().strftime("%H:%M:%S"))
    quit('Quitting')


def add_text(winname, message, location=(35, 35), colour=(255, 255, 255)):

    try:
        cv2.putText(img=winname,
                    text=message,
                    org=location,
                    color=colour,
                    fontScale=1,
                    fontFace=FONT)

    except KeyboardInterrupt:
        exit_sequence()

    except Exception as e:
        text_log(f'Failed to display {message} on {winname}. Exception - {e}',
                 curr_time=datetime.now().strftime("%H:%M:%S"),
                 show_console=True)


print('Starting...')

while True:
    find_face()
