import numpy as np
import cv2 as cv


def get_frames():
    cap = cv.VideoCapture('test.mp4')
    while True:
        isTrue, frame = cap.read()

        resized = cv.resize(frame, (int(frame.shape[1] * 0.7), int(frame.shape[0] * 0.7)),
                            interpolation=cv.INTER_CUBIC)

        cv.imshow('Video', resized)
        if cv.waitKey(16) & 0xFF == ord('s'):
            cv.imwrite('frame.jpg', resized)
            print("[MAIN] Exiting program...")
            break
    cap.release()
    cv.destroyAllWindows()

get_frames()