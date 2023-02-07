import dlib
import cv2
from imutils import face_utils
import numpy as np
from scipy.spatial import distance as dist
from time import time
from logging import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 0, 150)
GREEN = (0, 150, 0)

VID = cv2.VideoCapture(0)
# VID.set(cv2.CAP_PROP_SETTINGS, 0)
# VID.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
# VID.set(cv2.CAP_PROP_CONTRAST, 0.5)
# VID.set(cv2.CAP_PROP_EXPOSURE, 0.5)

YAWN_THRESH = 35
BLINK_THRESH = 0.16

DETECTOR = dlib.get_frontal_face_detector()
PREDICTOR = dlib.shape_predictor("data/shape_predictor_68_face_landmarks.dat")
HAAR_DATA = cv2.CascadeClassifier('data/frontfacedata.xml')
FONT = cv2.FONT_HERSHEY_SIMPLEX

# Debugging
DEBUG_FACE = True
DEBUG_EAR = True
DEBUG_EYES = False
DEBUG_LIPS = False


def exit_sequence() -> None:
    cv2.destroyAllWindows()
    # del DETECTOR, PREDICTOR, HAAR_DATA, DEBUG_FACE, DEBUG_LANDMARKS, DEBUG_BLINK, CLEAR_OLD_LOGS

    text_log(message='Quit',
             curr_time=datetime.now().strftime("%H:%M:%S"))

    quit('Quitting')


def find_face() -> list:

    ret, frame_ = VID.read()

    if ret:
        grayscale = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)
        face_coordinates = HAAR_DATA.detectMultiScale(image=grayscale,
                                                      scaleFactor=2,
                                                      minNeighbors=5,
                                                      minSize=(50, 50)
                                                      )

        if len(face_coordinates) == 1:
            x, y, w, h = [each for each in face_coordinates[0]]
            subframe = grayscale[y: y + h, x: x + w]

        else:
            x, y = 0, 0
            w = grayscale.shape[1]
            h = grayscale.shape[0]
            subframe = grayscale

        if DEBUG_FACE:
            cv2.imshow('Subframe', subframe)

        return [frame_, subframe, [x, y, x+w, y+h]]


def add_text(winname, message, location=(35, 35), colour=(255, 255, 255), thick=1, size=1.0) -> None:
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


def eye_aspect_ratio(eye) -> float:

    a = dist.euclidean(eye[1], eye[5])
    b = dist.euclidean(eye[2], eye[4])
    c = dist.euclidean(eye[0], eye[3])

    ear = (a + b) / (2.0 * c)

    return round(ear, 2)


def final_ear(shape) -> list:

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]

    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)

    ear = (leftEAR + rightEAR) / 2.0

    return [ear, leftEye, rightEye]


def lip_distance(shape) -> float:
    top_lip = shape[50:53]
    top_lip = np.concatenate((top_lip, shape[61:64]))

    low_lip = shape[56:59]
    low_lip = np.concatenate((low_lip, shape[65:68]))

    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)

    dst = abs(top_mean[1] - low_mean[1])

    return dst


def blink_yawn(sub_frame) -> list:

    blinked = False
    yawned = False
    lip = None
    lt_hull, rt_hull = None, None

    points = HAAR_DATA.detectMultiScale(image=frame,
                                        scaleFactor=2,
                                        minNeighbors=5,
                                        minSize=(50, 50)
                                        )

    for (x, y, w, h) in points:

        rectangle = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        shape = PREDICTOR(sub_frame, rectangle)
        shape = face_utils.shape_to_np(shape)

        # EYES -----------------------------------------------------------

        eye = final_ear(shape)
        ear = eye[0]
        print(ear)
        lt_eye = eye[1]
        rt_eye = eye[2]

        if DEBUG_EYES:
            lt_hull = cv2.convexHull(lt_eye)
            rt_hull = cv2.convexHull(rt_eye)

        # cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        # cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        # cv2.putText(frame, f'EAR: {ear}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if ear < BLINK_THRESH:
            blinked = True

        # MOUTH ---------------------------------------------------------

        distance = lip_distance(shape)

        lip = shape[48:60]
        '''
        cv2.drawContours(image=frame,
                         contours=[lip],
                         contourIdx=-1,
                         color=(200, 200, 200),
                         thickness=-1)
        '''
        if distance > YAWN_THRESH:
            yawned = True

    return [blinked, yawned, lt_hull, rt_hull, lip]


blink_ctr = 0
yawn_ctr = 0
temp_blink = 0
temp_yawn = 0
delta = 3
score = 100
adder = 0

init = time()

while True:

    # face_data = find_face()
    frame, subframe, box = find_face()

    blink = blink_yawn(subframe)[0]
    yawn = blink_yawn(subframe)[1]

    if blink:
        blink_ctr += 1
        temp_blink += 1

    if yawn:
        yawn_ctr += 1
        temp_yawn += 1

    # EYES CLOSED ----------------------------------
    if (time() - init <= delta) and temp_yawn >= 20:
        score -= 5
        temp_yawn = 0

    # YAWNING ---------------------------------------
    if (time() - init <= delta) and temp_blink >= 15:
        score -= 10
        temp_blink = 0

    if time() - init >= delta:
        init = time()
        adder += 1

    if adder % ((60/delta) * 10) == 0 and score <= 95:
        score += 5

    cv2.rectangle(img=frame,
                  pt1=(box[0], box[1]),
                  pt2=(box[2], box[3]),
                  color=WHITE,
                  thickness=2)

    add_text(winname=frame,
             message=f'Blinks {blink_ctr} Yawns {yawn_ctr} Score {score}',
             colour=WHITE,
             size=0.5,
             thick=2)

    add_text(winname=frame,
             message=f'Time {time}, Adder {adder}, Temp Blink/Yawn {temp_blink, temp_yawn}',
             location=(35, 70),
             size=0.5,
             thick=2)

    cv2.imshow('Frame', frame)
    cv2.waitKey(1)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break

cv2.destroyAllWindows()
