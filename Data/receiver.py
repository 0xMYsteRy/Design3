from tkinter import *
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import socket
import threading

HOST = '192.168.54.23'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

window = Tk()  # OPEN OF WINDOW

counter = 0


def process_data_from_server(x):
    x1, y1, z1 = x.split(",")
    return x1, y1, z1


humidvar = StringVar()
temperaturevar = StringVar()
moisturevar = StringVar()

new_humidvar = StringVar()
new_temperaturevar = StringVar()
new_moisturevar = StringVar()


def my_client():
    global humidvar, temperaturevar, moisturevar
    global new_humidvar, new_temperaturevar, new_moisturevar

    threading.Timer(11, my_client).start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # my = input("Enter command ")

        my = "Data"

        my_inp = my.encode('utf-8')

        s.sendall(my_inp)

        data = s.recv(1024).decode('utf-8')

        x_humid, y_temp, z_moisture = process_data_from_server(data)

        print("Before: ")
        print("Humidity {}".format(x_humid))
        print("Temperature {}".format(y_temp))
        print("Moisture {}".format(z_moisture))

        humidvar.set(x_humid)
        temperaturevar.set(y_temp)
        moisturevar.set(z_moisture)

        print("After: ")
        print("Humid {}".format(humidvar.get()))
        print("Temperature {}".format(temperaturevar.get()))
        print("Moisture {}".format(moisturevar.get()))

        time.sleep(5)
        new_humidvar.set("55")
        new_temperaturevar.set("28")
        new_moisturevar.set(z_moisture)

        print("After2: ")
        print("Humid {}".format(new_humidvar.get()))
        print("Temperature {}".format(new_temperaturevar.get()))
        print("Moisture {}".format(new_moisturevar.get()))

        time.sleep(1)

my_client()

def scan():  # QR scanning function
    global counter
    cap = cv2.VideoCapture(0)  # capture video  from default camera
    font = cv2.FONT_HERSHEY_PLAIN

    # set width, hight and the position of the pop-up windown
    cap.set(3, 640)
    cap.set(4, 640)

    # open and read the text file, which contains the list of registered people
    with open('list.text') as f:
        myList = f.read().splitlines()

    while True:
        _, frame = cap.read()
        for barcode in decode(frame):
            # convert to the original data
            myData = barcode.data.decode('utf-8')
            print(myData)

            # if-else statement to check the registed people
            if myData in myList:
                print("welcome")
                counter += 1
                print(counter)
                time.sleep(5)


            else:
                print('You are not registered')
                time.sleep(3)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(20) & 0xFF == ord('d'):
            break

    cap.release()
    cv2.destroyAllWindows()


#################################

def change_text():
    humidvar.set(new_humidvar.get())
    temperaturevar.set(new_temperaturevar.get())
    moisturevar.set(new_moisturevar.get())
    window.after(5000, change_text)  # 5000 is `equivalent to 5 second (closest you'll get)

# change_text()  # to start the update loop



# humid
humidLabel = Label(window, text="Humidity: ").grid(row=0, column=0)
humid = Label(window, text=str((humidvar.get())), width=50, borderwidth=20).grid(row=1, column=0)

# temp
tempLabel = Label(window, text="Temperature: ").grid(row=0, column=1)
temp = Label(window, text=str(temperaturevar.get()), width=50, borderwidth=20).grid(row=1, column=1)

# moisture
moistureLabel = Label(window, text="Moisture").grid(row=0, column=2)
moisture = Label(window, text=str(moisturevar.get()), width=50, borderwidth=20).grid(row=1, column=2)

# no people
noPplLabel = Label(window, text="Number of people").grid(row=0, column=3)
noPpl = Label(window, text="0", width=50, borderwidth=20).grid(row=1, column=2)

but1 = Button(window, text="Human Detection Livestream", width=30, font=("Ariel Bold", 15), bg='blue').grid(row=2,
                                                                                                            column=0)
but2 = Button(window, text="Update status", width=30, font=("Ariel Bold", 15), bg='blue',command=lambda: change_text()).grid(row=2, column=1)

but3 = Button(window, text="SCAN QR CODE", width=30, font=("Ariel Bold", 15), bg='blue', command=lambda: scan()).grid(
    row=2, column=2)


window.mainloop()