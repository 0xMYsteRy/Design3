#!/usr/bin/env python
import threading
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

def pirMotionDetect():
    # import sys
    #
    # if len(sys.argv) < 2:
    #     print('Usage: {} pin'.format(sys.argv[0]))
    #     sys.exit(1)

    # pir = GroveMiniPIRMotionSensor(int(sys.argv[1]))

    # Pir sensor use pin 12
    pir = GroveMiniPIRMotionSensor(12)

    def callback():
        print('Motion detected.')

    pir.on_detect = callback

    while True:
        time.sleep(1)

def ultraSonicDetect():
    # Grove - Ultrasonic Ranger connected to port D5
    sensor = GroveUltrasonicRanger(5)

    while True:
        distance = sensor.get_distance()
        print('{} cm'.format(distance))

        time.sleep(1)

if __name__ == '__main__':
    t1 = threading.Thread(target=pirMotionDetect(), name='MotionDetect')
    t2 = threading.Thread(target=ultraSonicDetect(), name='DistanceDetect')

    # Running multi threads
    t1.start()
    t2.start()

    # Wait threads
    t1.join()
    t2.join()