from flask import Flask, render_template, Response
import cv2
from pyzbar.pyzbar import decode  # QR code
from grove.display.jhd1802 import JHD1802  # LCD

app = Flask(__name__, template_folder='template')
camera = cv2.VideoCapture(0)


def generate_frames():
    with open('list.text') as f:
        myList = f.read().splitlines()

    while True:

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

                else:
                    lcd.write('InValid QRcode')
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)