import socket
import time
import seeed_dht

HOST = '192.168.31.237'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def receive_data():
    # for DHT11/DHT22, pin 18
    sensor = seeed_dht.DHT("11", 18)

    # while True:
    humi, temp = sensor.read()
    if not humi is None:
        print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(sensor.dht_type, humi, temp))
        data = '{},{}'.format(humi, temp)
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
        my_server()