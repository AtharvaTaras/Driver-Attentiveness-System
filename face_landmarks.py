import cv2
import dlib

image = cv2.imread("data/testimg.jpeg")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("data/shape_predictor_68_face_landmarks.dat")

'''
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = detector(gray)

for face in faces:
    landmarks = predictor(gray, face)

    for n in range(0, 68):
        x = landmarks.part(n).x
        y = landmarks.part(n).y
        cv2.circle(image, (x, y), 1, (255, 0, 0), -1)

cv2.imshow("Facial Landmarks", image)
cv2.waitKey(0)
'''

vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)

            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)
                cv2.putText(img=frame,
                            text=str(n),
                            org=(x, y),
                            fontFace=cv2.FONT_HERSHEY_PLAIN,
                            fontScale=1,
                            thickness=1,
                            color=(255, 255, 255))

            frame = cv2.resize(frame, dsize=(frame.shape[1] * 2, frame.shape[0] * 2))
            cv2.imshow("Facial Landmarks", frame)
            cv2.waitKey(1)
