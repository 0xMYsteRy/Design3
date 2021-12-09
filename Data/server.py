import socket
import time
import seeed_dht
import math
import sys
from grove.adc import ADC

#gui module
fomr tkinter import *


HOST = '192.168.31.237'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

class GroveMoistureSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
    @property
    def moisture(self):
        value = self.adc.read_voltage(self.channel)
        return value

Grove = GroveMoistureSensor

def receive_data():

    # humidity and temperature sensor
    # for DHT11/DHT22, pin 18
    sensor = seeed_dht.DHT("11", 18)

    # moisture sensor
    from grove.helper import SlotHelper
    sh = SlotHelper(SlotHelper.ADC)

    #pin = sh.argv2pin()
    # Normally plug in pin4
    pin = 4
    sensor2 = GroveMoistureSensor(pin)

    # while True:
    humi, temp = sensor.read()
    m = sensor2.moisture

    # Testing moisture value
    if 0 <= m and m < 300:
        result = 'Dry'
    elif 300 <= m and m < 600:
        result = 'Moist'
    else:
        result = 'Wet'
    print('Moisture value: {0}, {1}'.format(m, result))

    if not humi is None:
        print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*, moisture{1}'.format(sensor.dht_type, humi, temp, result))
        data = '{},{},{}'.format(humi, temp, result)
        return data

    else:
        print('DHT{0}, humidity & temperature: {1}'.format(sensor.dht_type, temp))

    time.sleep(1)


def my_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Waiting client for connection ... ")
        s.bind((HOST, PORT))
        s.listen(5)
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:

                data = conn.recv(1024).decode('utf-8')

                if str(data) == "Data":

                    print("Ok Sending data ")

                    my_data = receive_data()

                    x_encoded_data = my_data.encode('utf-8')

                    conn.sendall(x_encoded_data)

                elif str(data) == "Quit":
                    print("shutting down server ")
                    break

                if not data:
                    break
                else:
                    pass


if __name__ == '__main__':
    while 1:
        window = Tk()
        window.Title(text = "Control station")

        temp = Label()
        my_server()