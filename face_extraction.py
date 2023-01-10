import cv2

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
        # print(type(face_coordinates))

        if face_coordinates != ():
            for each in face_coordinates:
                x = each[0]
                y = each[1]
                w = each[2]
                h = each[3]

            subframe = grey[y: y+h, x: x+w]

            cv2.imshow('Face', subframe)

        cv2.imshow('Cam', frame)
        cv2.waitKey(1)

    else:
        print('No video feed detected')
        cv2.destroyAllWindows()
