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
from seeed_dht import DHT  # Temperature & Humidity

from time import sleep


def displayData():
    # Grove - Ultrasonic Ranger connected to port D5 and D18
    sensor1 = GroveUltrasonicRanger(5)
    sensor2 = GroveUltrasonicRanger(16)

    # Grove - Relay connected to port D16
    relay = GroveRelay(22)

    # Grove - Moisture Sensor connected to port A0
    sensor3 = GroveMoistureSensor(0)

    # Grove - Temperature&Humidity Sensor connected to port D5
    sensor4 = DHT('11', 26)

    while True: