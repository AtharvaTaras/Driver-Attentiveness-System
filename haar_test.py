import cv2
import winsound

HAAR_DATA = cv2.CascadeClassifier('data/frontfacedata.xml')
VID = cv2.VideoCapture(0)
# VID.set(cv2.CAP_PROP_EXPOSURE, -4)
VID.set(cv2.CAP_PROP_BRIGHTNESS, 150)
VID.set(cv2.CAP_PROP_CONTRAST, 100)
VID.set(cv2.CAP_PROP_GAMMA, 15)

while True:
    _, frame = VID.read()
    x, y, w, h = 0, 0, 0, 0

    if _:
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_coordinates = HAAR_DATA.detectMultiScale(image=grey,
                                                      scaleFactor=2,
                                                      minNeighbors=5,
                                                      minSize=(50, 50)
                                                      )

        if len(face_coordinates) == 1:
            x, y, w, h = [each for each in face_coordinates[0]]
            print(x, y, w, h)

        cv2.rectangle(frame,
                      pt1=(x-25, y-25),
                      pt2=(x+w+25, y+h+25),
                      thickness=5,
                      color=(0, 0, 0))

        cv2.imshow('frame', frame)
        cv2.waitKey(1)


