import time
import easygui
import cv2
import numpy as np

from grove.grove_relay import GroveRelay  # Relay
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger  # Ultrasonic sensor
from gpiozero import Buzzer  # buzzer
from pyzbar.pyzbar import decode  # QR code
from grove.display.jhd1802 import JHD1802  # LCD
from tkinter import *  # UI
from grove.grove_moisture_sensor import GroveMoistureSensor  # Moisture
# from seeed_dht import DHT  # Temperature & Humidity
import globals
from time import sleep

# people counting flags
flag_enter1 = 0
flag_enter2 = 0
flag_exit1 = 0
flag_exit2 = 0
# QR code trigger
flag_qr = 0
# QR code countdown
flag_qr_count = 0
# Environmental data trigger
flag_env = 2

red = Buzzer(24)

# capture video from default camera
cap = cv2.VideoCapture(0)

###############FRAME SIZE FOR CAMERA######################
# set width, hight and the position of the pop-up windown
cap.set(3, 640)
cap.set(4, 640)

# open and read the text file, which contains the list of registered people
with open('list.text') as f:
    myList = f.read().splitlines()


#############################MAIN FUNCTION#######################
def main():
    # Grove - Ultrasonic Ranger connected to port D5 and D18
    sensor1 = GroveUltrasonicRanger(5)
    sensor2 = GroveUltrasonicRanger(16)

    # Grove - Relay connected to port D16
    relay = GroveRelay(22)

    # Grove - Moisture Sensor connected to port A0
    sensor3 = GroveMoistureSensor(0)

    # Grove - Temperature&Humidity Sensor connected to port PWM
    #sensor4 = DHT('11', 12)

    global flag_enter1, flag_enter2
    global flag_exit1, flag_exit2
    global flag_qr, flag_qr_count, flag_env

    # if flag_env == 2:
        # ################Temp & Humidity Detection######
        # humi, temp = sensor4.read()
        # print('\ntemperature {}C, humidity {}%'.format(temp, humi))
        #
        # ################MOISTURE Detection########################
        # mois = sensor3.moisture
        # if 0 <= mois and mois < 300:
        #     level = 'dry'
        # elif 300 <= mois and mois < 600:
        #     level = 'moist'
        # else:
        #     level = 'wet'
        # print('moisture: {}, {}\n'.format(mois, level))
        # flag_env = 0

    distance1 = sensor1.get_distance()
    print('Ultra 1 {} cm'.format(distance1))

    distance2 = sensor2.get_distance()
    print('Ultra 2 {} cm'.format(distance2))

    if distance1 < 60 and flag_exit1 == 0:
        relay.on()
        # relay
        print('relay on')
        time.sleep(0.1)
        relay.off()
        print('relay off')
        flag_enter1 = 1
    if flag_enter1 == 1 and distance2 < 60:
        flag_enter2 = 1

    if distance2 < 60 and flag_enter1 == 0:
        relay.on()
        # relay
        print('relay on')
        time.sleep(0.1)
        relay.off()
        print('relay off')
        flag_exit1 = 1
    if flag_exit1 == 1 and distance1 < 60:
        flag_exit2 = 1

    if flag_enter1 == 1 and flag_enter2 == 1:
        globals.enter_Counter = globals.enter_Counter + 1
        flag_qr = 1

        time.sleep(0.8)
        flag_enter1 = 0
        flag_enter2 = 0

    if flag_exit1 == 1 and flag_exit2 == 1:
        globals.exit_Counter = globals.exit_Counter + 1
        time.sleep(0.8)
        flag_exit1 = 0
        flag_exit2 = 0
    # Unexpected exit person
    if globals.exit_Counter > globals.enter_Counter:
        red.on()
        sleep(0.03)
        red.off()
        sleep(0.03)
        easygui.msgbox("Unexpected Exit detected!", title="Warning")
        globals.exit_Counter = globals.exit_Counter - 1

    Current_people = globals.enter_Counter - globals.exit_Counter
    # Buzzer sound 5 times when the room is full
    if Current_people > 5:
        red.on()
        sleep(0.05)
        red.off()
        sleep(0.05)
    if Current_people < 6:
        red.off()
        sleep(0.1)

        # Displaying current information
    print("Enter_Total:%s\n" % globals.enter_Counter)
    print("Exit_Total:%s\n" % globals.exit_Counter)
    print("CurrentPeople:%s\n" % (Current_people))
    time.sleep(0.05)

    ################QR + CAMERA + LCD########################
    while (flag_qr == 1):

        flag_qr_count = flag_qr_count + 1  # QR camera timer

        cap.set(3, 640)  # QR code camera on again
        cap.set(4, 640)
        success, image = cap.read()  # get image from webcam

        if success == True:
            # show capture image on a window, updating time depends on waitKey
            cv2.imshow('Result', image)
            cv2.waitKey(1)

            for barcode in decode(image):

                # convert to the original data
                myData = barcode.data.decode('utf-8')
                print(myData)

                # Grove - 16x2 LCD(White on Blue) connected to I2C port
                lcd = JHD1802()

                lcd.setCursor(0, 0)

                # if-else statement to check the registed people
                if myData in myList:
                    lcd.write('Valid QRcode')
                    # Close camera window
                    cv2.destroyAllWindows()
                    flag_qr = 0
                    flag_env = 1
                    red.on()
                    sleep(0.05)
                    red.off()
                    sleep(0.05)
                    flag_qr_count = 0

                else:
                    lcd.write('Invalid QRcode')
                    red.on()
                    sleep(0.3)
                    red.off()
                    sleep(0.3)
                    flag_qr_count = 0
                    # Close camera window
                    cv2.destroyAllWindows()
                    flag_qr = 0
                    flag_env = 1
                    # globals.enter_Counter = globals.enter_Counter - 1



            if flag_qr_count == 152:
                red.on()
                sleep(0.1)
                red.off()
                sleep(0.1)
                red.on()
                sleep(0.1)
                red.off()
                sleep(0.1)
                lcd = JHD1802()
                lcd.setCursor(0, 0)
                lcd.write('Overtime, re-enter')
                # Close camera window
                cv2.destroyAllWindows()
                flag_qr = 0
                flag_env = 1
                flag_qr_count = 0
                globals.enter_Counter = globals.enter_Counter - 1


if __name__ == '__main__':
    main()
