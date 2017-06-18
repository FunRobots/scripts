import cv2
import sys
import time

cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('face_video.avi', fourcc, 8.0, (640,480))
start = time.time()
while time.time() - start < 20:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        print('x:', x, 'y:', y, 'w:', w, 'h:', h)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    out.write(frame)
    #cv2.imshow('Video', frame)
out.release()

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
