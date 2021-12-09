#!/usr/bin/env python
import time
from grove.gpio import GPIO
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger


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


def peopleDetection():
    # number of people detect
    number_of_people = 0

    # first we test with the ultra sonic sensor
    # if people passes 2 sensors then count the number of people in the room
    sensor = GroveUltrasonicRanger(5)
    while True:
        distance1 = sensor.get_distance()
        print('{} cm'.format(distance1))

        time.sleep(1)
        distance2 = sensor.get_distance()
        print('{} cm'.format(distance2))

        # Check the people going in
        if (distance2 > distance1):
            lastestDistance = distance2 - distance1

            # Distance between from people walking out and in is 2 meter
            if (lastestDistance > 200):
                print("Test OK")

                # Then test with the pir sensor
                # pir dectection
                pir = GroveMiniPIRMotionSensor(12)

                def callback():
                    print('Motion detected. \n')


                pir.on_detect = callback

                # Pass 2 sensors then count up the number of people
                number_of_people += 1
                print("Current number of people in the room: ")
                print(number_of_people)

                if (number_of_people >= 5):
                    print("Exceed maximum number of people in the room")
                    # Transfer the task to QR code in task 2

                while True:
                    time.sleep(1)

        time.sleep(1)

    # Check if can execute this loop
    print("No infinite loop")

    while True:
        def callback():
            print('Motion detected.')

        pir.on_detect = callback
        print('Pass this test case')
        print('Current number of people: ')
        print(number_of_people)

        # Get the second sensor to work
        sensor = GroveUltrasonicRanger(5)
        while True:
            distance1 = sensor.get_distance()
            print('{} cm'.format(distance1))

            time.sleep(1)
            distance2 = sensor.get_distance()
            print('{} cm'.format(distance2))

            if (distance1 > distance2):
                lastestDistance = distance1 - distance2

                # Distance between from people walking out and in is 1 meter
                if (lastestDistance > 100):
                    print("Test OK")
                    number_of_people -= 1

                    #Testing
                    print("Current number of people in the room: ")
                    print(number_of_people)

                    if (number_of_people == 0):
                        print("Room is empty")

        while True:
            time.sleep(1)

if __name__ == '__main__':
    peopleDetection();
