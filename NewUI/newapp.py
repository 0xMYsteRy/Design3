import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response, Response
from grove.grove_moisture_sensor import GroveMoistureSensor
from seeed_dht import DHT
import cv2
from pyzbar.pyzbar import decode # QR code
from grove.display.jhd1802 import JHD1802  # LCD

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    with open('list.text') as f:
        myList = f.read().splitlines()

    while True:

        validcode = 0
        ## read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            for barcode in decode(frame):
                myData = barcode.data.decode('utf-8')
                # Grove - 16x2 LCD(White on Blue) connected to I2C port
                lcd = JHD1802()
                lcd.setCursor(0, 0)

                if myData in myList:
                    lcd.write('Valid QRcode')
                    validcode = 1

                else:
                    lcd.write('InValid QRcode')

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/data', methods=["GET", "POST"])
def data():

    # Three sensors
    # Grove - Moisture Sensor connected to port A0
    sensor3 = GroveMoistureSensor(0)

    # Grove - Temperature&Humidity Sensor connected to port D5
    sensor4 = DHT('11', 26)

    humi, temp = sensor4.read()
    print('\ntemperature {}C, humidity {}%'.format(temp, humi))

    mois = sensor3.moisture
    if 0 <= mois and mois < 300:
        level = 'dry'
    elif 300 <= mois and mois < 600:
        level = 'moist'
    else:
        level = 'wet'
    print('moisture: {}, {}\n'.format(mois, level))

    #Temperature = random() * 100
    #Humidity = random() * 55
    #Moisture = random() * 60


    PersonIn = random() * 5
    PersonOut = random() * 5

    validcode = generate_frames

    #PersonIn = full.Enter_Counter
    #PersonOut = full.Exit_Counter
    data = [time() * 1000, temp, humi, mois, PersonIn, PersonOut, validcode]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

