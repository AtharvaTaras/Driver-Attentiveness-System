import time
import dlib
import cv2
from imutils import face_utils
import numpy as np
from scipy.spatial import distance as dist

detector = cv2.CascadeClassifier(r'data/frontfacedata.xml')
predictor = dlib.shape_predictor(r'data/shape_predictor_68_face_landmarks.dat')

vid = cv2.VideoCapture(0)


def lip_distance(shape):
    top_lip = shape[50:53]
    top_lip = np.concatenate((top_lip, shape[61:64]))

    low_lip = shape[56:59]
    low_lip = np.concatenate((low_lip, shape[65:68]))

    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)

    distance = abs(top_mean[1] - low_mean[1])

    return distance


while True:

    ret, frame = vid.read()

    if ret:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        points = detector.detectMultiScale(image=gray,
                                           scaleFactor=1.1,
                                           minNeighbors=5,
                                           minSize=(30, 30),
                                           flags=cv2.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in points:
            rectangle = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))

            shape = predictor(gray, rectangle)
            shape = face_utils.shape_to_np(shape)

            distance = lip_distance(shape)

            lip = shape[48:60]
            cv2.drawContours(image=frame,
                             contours=[lip],
                             contourIdx=-1,
                             color=(200, 200, 200),
                             thickness=-1)

        cv2.imshow('frame', frame)
        cv2.waitKey(1)

cv2.destroyAllWindows()
