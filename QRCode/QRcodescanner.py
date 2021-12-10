import cv2
from pyzbar.pyzbar import decode
from tkinter import *
import numpy as np
import time
import sys
import os

from grove.display.jhd1802 import JHD1802

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

root = Tk()



# capture video from default camera
cap = cv2.VideoCapture(0)

# set width, hight and the position of the pop-up windown
cap.set(3, 640)
cap.set(4, 640)

# open and read the text file, which contains the list of registered people
with open('list.text') as f:
    myList = f.read().splitlines()

# while looop for the main process
while True:
    success, img = cap.read()

    for barcode in decode(img):

        # convert to the original data
        myData = barcode.data.decode('utf-8')
        print(myData)

        # if-else statement to check the registed people
        if myData in myList:

            #print('Welcome')
            lcd = JHD1802()

            lcd.setCursor(0, 0)
            lcd.write('Welcome aboard! ')
            time.sleep(3)
        else:
            lcd = JHD1802()
            lcd.write('Your not allow! ')
            print('GTFO!')

        # draw a border for the QR code
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 0, 255), 5)

    # show capture image on a window, updating time depends on waitKey
    cv2.imshow('Result', img)
    cv2.waitKey(1)

root.mainloop()