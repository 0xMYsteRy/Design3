import socket
import time


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

def server_program():

    # change this
    host = '192.168.1.10'
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = receive_data()
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()