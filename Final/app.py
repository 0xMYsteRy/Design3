import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
from grove.grove_moisture_sensor import GroveMoistureSensor
from seeed_dht import DHT

import globals
import resources

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    globals.initialize()
    # Data Format
    # [TIME, Temperature, Humidity]

    # Grove - Moisture Sensor connected to port A0
    # sensor3 = GroveMoistureSensor(0)

    # Grove - Temperature&Humidity Sensor connected to port PWM
    #sensor4 = DHT('11', 12)

    #humidity, temperature = sensor4.read()
    # print('\ntemperature {}C, humidity {}%'.format(temperature, humidity))

    # moisture = sensor3.moisture
    # if 0 <= moisture and moisture < 300:
    #     level = 'dry'
    # elif 300 <= moisture and moisture < 600:
    #     level = 'moist'
    # else:
    #     level = 'wet'
    # print('moisture: {}, {}\n'.format(moisture, level))

    temperature = random() * 100
    humidity = random() * 55
    moisture = random() * 60
    # PersonIn = random() * 5
    # PersonOut = random() * 5
    # Temperature = resources.Temperature
    # Humidity = resources.Humidity
    # Moisture = resources.Moisture
    # Enter_Counter = resources.Enter_Counter
    # Exit_Counter = resources.Exit_Counter
    print(globals.enter_Counter, globals.exit_Counter)

    resources.main()

    data = [time(), temperature, humidity, moisture, globals.enter_Counter, globals.exit_Counter]
    #data = [time() * 1000, temp, humi, mois, PersonIn, PersonOut]


    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)