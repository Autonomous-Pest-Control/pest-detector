import socket
import sys
import toml

from detection_message import MESSAGE_LENGTH, DetectionMessage
from controller import Controller

CMD_CLOCKWISE = 1
CMD_COUNTER_CLOCKWISE = 2
CMD_STOP = 3

DEVICE_NAME_WIN = 'COM6'
DEVICE_NAME_LINUX = '/dev/ttyX'

config = toml.load('../Config.toml')

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_hostname = config['edge_server']['ip']
server_port = int(config['edge_server']['detection']['port'])
print(f'Attempting connection to {server_hostname}:{server_port}')
sock.connect((server_hostname, server_port))
print(f'Connected to {server_hostname}:{server_port}')

controller = Controller()

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

        controller.send_command(CMD_CLOCKWISE, 0)

    except socket.timeout:
        pass
    except socket.error:
        e = sys.exc_info()[1]
        print(f'Socket error: errno={e}. Terminating...')
        break