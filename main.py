import cv2
import dlib
from datetime import datetime
from time import time, sleep
import numpy as np
from logging import *
text_log(message='Imported libraries successfully.',
         show_console=True)

# Global Constants

DEBUG_FACE = False
DEBUG_LANDMARKS = True
CLEAR_OLD_LOGS = False
DETECTOR = dlib.get_frontal_face_detector()
PREDICTOR = dlib.shape_predictor("data/shape_predictor_68_face_landmarks.dat")
HAAR_DATA = cv2.CascadeClassifier('data/frontfacedata.xml')
FONT = cv2.FONT_HERSHEY_SIMPLEX
VID = cv2.VideoCapture(1)

if CLEAR_OLD_LOGS:
    clear_logs()

text_log(message='Global variables set.')


def find_face(avearges: list) -> list:

    ret, frame = VID.read()
    drowsy = False
    blinks = 0
    yawns = 0

    if ret:
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_coordinates = HAAR_DATA.detectMultiScale(grayscale)

        if len(face_coordinates) == 4:
            x, y, w, h = (each for each in face_coordinates)
            # return [x, y, x + w, y + h]  # Face Mask

            # subframe = grayscale[y: y + h, x: x + w]
            subframe = grayscale

            faces = DETECTOR(subframe)
            lt = []
            rt = []
            points = []

            for face in faces:
                landmarks = PREDICTOR(subframe, face)

                for n in range(0, 68):
                    y = landmarks.part(n).y
                    points.append(y)

                lt = points[36:42]
                rt = points[42:48]

                if (sum(lt)/len(lt) < avearges[0]) or (sum(rt)/len(rt) < avearges[1]):
                    drowsy = True

                else:
                    drowsy = False

            cv2.imshow('Main', frame)
            add_text(winname=frame,
                     message=f'Drowsy:{drowsy}')
            cv2.waitKey(1)

        else:
            x, y, w, h = 0, 0, 0, 0

            cv2.imshow('Main', frame)
            add_text(winname=frame,
                     message=f'Drowsy:{drowsy}')
            cv2.waitKey(1)

        if DEBUG_FACE:
            cv2.imshow('Raw Input', frame)
            cv2.rectangle(img=grayscale,
                          pt1=(x, y),
                          pt2=(x+h, y+w),
                          thickness=1,
                          color=(255, 255, 255))
            cv2.imshow('Grayscale', grayscale)
            #cv2.imshow('Extracted Face', subframe)
            cv2.waitKey(1)
            # print(face_coordinates)


def check_blink():
    pass


def check_yawn():
    pass


def facial_landmarks():
    pass


def calibrate(duration: float) -> list:
    ret, frame = VID.read()

    if ret:
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = DETECTOR(grey)
        # frame = cv2.resize(frame, dsize=(frame.shape[1] * 2, frame.shape[0] * 2))

        lt_eye = []
        rt_eye = []

        start = time()

        while True:

            for face in faces:
                landmarks = PREDICTOR(grey, face)

                points = []

                for n in range(0, 68):

                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    # Appending Y coordinates only since we need vertical euclidean distance between eyelids/lips
                    points.append(y)
                    # print(points)

                    if ((n > 35) and (n < 48)) or ((n > 47) and (n < 68)):

                        if DEBUG_LANDMARKS:
                            cv2.circle(frame,
                                       center=(x, y),
                                       radius=2,
                                       color=(0, 0, 0),
                                       thickness=-1)

                            add_text(winname=frame,
                                     location=(x, y),
                                     message=str(n),
                                     colour=(255, 255, 255),
                                     size=0.25
                                     )

                add_text(winname=frame,
                         message='Calibrating system, please relax your face to a normal position',
                         thick=2,
                         size=0.5,
                         colour=(25, 25, 25)
                         )

                lt_avg = ((points[41] - points[37]) + (points[40] - points[38]))/2
                rt_avg = ((points[47] - points[43]) + (points[48] - points[44]))/2

                lt_eye.append(lt_avg)
                rt_eye.append(rt_avg)

                cv2.imshow("Facial Landmarks", frame)
                cv2.waitKey(1)

                if time()-start <= duration:
                    break

                break

                # print(lt_eye, rt_eye)

        cv2.destroyAllWindows()
        # Return average eyelid separation for both eyes
        return [sum(lt_eye)/len(lt_eye), sum(rt_eye)/len(rt_eye)]


def exit_sequence() -> None:
    cv2.destroyAllWindows()
    del DETECTOR, PREDICTOR, HAAR_DATA, DEBUG_FACE, DEBUG_LANDMARKS, CLEAR_OLD_LOGS

    text_log(message='Quit',
             curr_time=datetime.now().strftime("%H:%M:%S"))

    quit('Quitting')


def add_text(winname, message, location=(35, 35), colour=(255, 255, 255), thick=1, size=1.0):

    try:
        cv2.putText(img=winname,
                    text=message,
                    org=location,
                    color=colour,
                    fontScale=size,
                    fontFace=FONT,
                    thickness=thick)

    except KeyboardInterrupt:
        exit_sequence()

    except Exception as e:
        text_log(f'Failed to add text {message} on {winname}. Exception - {e}',
                 curr_time=datetime.now().strftime("%H:%M:%S"),
                 show_console=True)


text_log(message='All functions initialized, starting...',
         show_console=True)
avg_vals = calibrate(5.00)

while True:
    find_face(avg_vals)

