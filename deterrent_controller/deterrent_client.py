import socket
import sys
import threading
import toml

from detection_message import MESSAGE_LENGTH, DetectionMessage

config = toml.load('../Config.toml')

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_hostname = config['edge_server']['ip']
server_port = int(config['edge_server']['detection']['port'])
print(f'Attempting connection to {server_hostname}:{server_port}')
sock.connect((server_hostname, server_port))
print(f'Connected to {server_hostname}:{server_port}')

class_id = 0
x_loc = 0.0
while True:
    try:
        data = sock.recv(MESSAGE_LENGTH)
        if len(data) == 0:
            print("Error: failed to receive data. Terminating...")
            break

        detection = DetectionMessage.from_bytes(data)
        if detection is None:
            print("Error: received invalid message. Skipping...")
            continue

        print(f'Detected class {detection.class_id} at x={detection.x_loc}')
    except socket.timeout:
        pass
    except socket.error:
        e = sys.exc_info()[1]
        print(f'Socket error: errno={e}. Terminating...')
        break