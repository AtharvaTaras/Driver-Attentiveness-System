import cv2

WHITE = (255, 255, 255)
THICK = 10
VIDEO_FEED = 0
# 0 = Laptop Webcam
# 1 = External Webcam

dataset = cv2.CascadeClassifier('data/frontfacedata.xml')
vid = cv2.VideoCapture(VIDEO_FEED)

while True:

    ret, frame = vid.read()

    if ret:

        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_coordinates = dataset.detectMultiScale(grey)

        if face_coordinates == ():
            cv2.putText(frame,
                        text='Cannot detect face',
                        org=(15, 35),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=WHITE)

        for each in face_coordinates:
            x = each[0]
            y = each[1]
            w = each[2]
            h = each[3]

            cv2.rectangle(frame, (x, y), (x + w, y + h), color=WHITE, thickness=THICK)

        if VIDEO_FEED == 0:
            cv2.imshow('Web Cam', frame)

        else:
            cv2.imshow('External Cam', frame)

        cv2.waitKey(1)

    else:
        print('No video feed detected')
        cv2.destroyAllWindows()
