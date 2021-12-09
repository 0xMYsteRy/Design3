# !/usr/bin/env python
import threading
import time
from grove.gpio import GPIO
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

import socket

# Wifi stuff
BROKER_LOCATION = "192.168.0.1"
PORT=31337

class GroveMiniPIRMotionSensor(GPIO):
    def __init__(self, pin):
        super(GroveMiniPIRMotionSensor, self).__init__(pin, GPIO.IN)
        self._on_detect = None

    @property
    def on_detect(self):
        return self._on_detect

    @on_detect.setter
    def on_detect(self, callback):
        if not callable(callback):
            return

        if self.on_event is None:
            self.on_event = self._handle_event

        self._on_detect = callback

    def _handle_event(self, pin, value):
        if value:
            if callable(self._on_detect):
                self._on_detect()

Grove = GroveMiniPIRMotionSensor

def motionDectect():
    import sys

    if len(sys.argv) < 2:
        print('Usage: {} pin'.format(sys.argv[0]))
        sys.exit(1)

    #pir = GroveMiniPIRMotionSensor(int(sys.argv[1]))
    pir = GroveMiniPIRMotionSensor(15)

    def callback():
        print('Motion detected.')

    pir.on_detect = callback

    while True:
        time.sleep(1)


def distanceDetect():
    # Grove - Ultrasonic Ranger connected to port D8
    sensor = GroveUltrasonicRanger(8)

    while True:
        distance1 = sensor.get_distance()
        print('{} cm'.format(distance1))

        distance2 = sensor.get_distance()
        print('{} cm'.format(distance2))

        lastestDistance = distance2 - distance1;

        if (lastestDistance > 200):
            print("OK")

        time.sleep(3)


def numOfPeople():
    # Change number of people later
    people = 0;

    if numOfPeople is not None:
        print("data people{}".format(people))
        data = '{}'.format(people)
        return data

#Put on Ras3
def runServer():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server Started waiting for client to connect ")
        s.bind((BROKER_LOCATION, PORT))
        s.listen(5)
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:

                data = conn.recv(1024).decode('utf-8')

                if str(data) == "Data":

                    print("Sending data... ")

                    my_data = numOfPeople()

                    x_encoded_data = my_data.encode('utf-8')

                    conn.sendall(x_encoded_data)

                elif  str(data) == "Quit":
                    print("shutting down server ")
                    break


                if not data:
                    break
                else:
                    pass

#Put on client Machine
# import socket
# import threading
# import time
#
#
# HOST = '192.168.0.1'
# PORT = 31337
#
#
# def process_data_from_server(x):
#     # x = number of people
#     return x
#
# def my_client():
#     threading.Timer(11, my_client).start()
#
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((HOST, PORT))
#
#         my = input("Enter command ")
#
#         my_inp = my.encode('utf-8')
#
#         s.sendall(my_inp)
#
#         data = s.recv(1024).decode('utf-8')
#
#         x_numberofPeople = process_data_from_server(data)
#
#         print("Number of People {}".format(x_numberofPeople))
#         s.close()
#         time.sleep(5)

if __name__ == '__main__':

    # Create thread
    t1 = threading.Thread(target=motionDectect(), name='MotionDetect')
    t2 = threading.Thread(target=distanceDetect(), name='DistanceDetect')
    t3 = threading.Thread(target=runServer(), name='RunServer')

    # Running multi threads
    t1.start()
    t2.start()
    t3.start()

    # Wait threads
    t1.join()
    t2.join()
    t3.start()