import socket
import sys
import threading

SERVER_ADDR = '192.168.0.2'	# Symbolic name meaning all available interfaces
PORT = 5455	# Arbitrary non-privileged port

MAX_X_LOCATION_CHARS = 19
MAX_CLASS_ID_CHARS = 2
SEPARATOR_CHARS = 1
MAX_EXPECTED_DATA_LEN = MAX_CLASS_ID_CHARS + SEPARATOR_CHARS + MAX_X_LOCATION_CHARS

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_hostname = SERVER_ADDR
server_port = PORT
print(f'Attempting connection to {server_hostname}:{server_port}')
sock.connect((server_hostname, server_port))
print(f'Connected to {server_hostname}:{server_port}')

class_id = 0
x_loc = 0.0
while True:
    try:
        data = sock.recv(MAX_EXPECTED_DATA_LEN)
        message = data.decode("ascii")
        msg_fields = message.split(',')

        class_id = int(msg_fields[0])
        x_loc = float(msg_fields[1])

        print(f'Detected class {class_id} at x={x_loc}')
    except socket.timeout:
        pass
    except:
        print('Received invalid message')