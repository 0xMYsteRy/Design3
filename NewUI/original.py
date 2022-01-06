import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
from grove.grove_moisture_sensor import GroveMoistureSensor
from seeed_dht import DHT
# from data import *

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():

    # Data Format
    # [TIME, Temperature, Humidity]

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
    data = [time() * 1000, temp, humi, mois, PersonIn, PersonOut]

    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)