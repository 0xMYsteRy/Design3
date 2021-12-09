import socket
import time


def process_data_from_server(x):
    x1, y1 = x.split(",")
    return x1,y1

def client_program():

    # change this
    host = '192.168.1.10'
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'quit':

        data = client_socket.recv(1024).decode()  # receive response

        x_humid, y_temp = process_data_from_server(data)
        print("Humidity {}%".format(x_humid))
        print("Temperature {} ".format(y_temp))

        time.sleep(1)

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()
