import cv2
import numpy as np

pic = cv2.imread('data/testimg.jpeg')

cv2.line(pic, pt1=(10, 15), pt2=(15, 20), color=(0,0,0))

while True:
    cv2.imshow('img', pic)
    cv2.waitKey(1)

