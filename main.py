import cv2
from datetime import date, datetime

import numpy as np

from logging import *
print('Imported libraries successfully.')

# Global Constants

HAAR_DATA = cv2.CascadeClassifier('data/frontfacedata.xml')
DEBUG = False
PAD_SIZE = 10
VID = cv2.VideoCapture(0)


def find_face() -> None:
    pass

