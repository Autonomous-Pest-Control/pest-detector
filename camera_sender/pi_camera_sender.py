from vidgear.gears import VideoGear
from vidgear.gears import NetGear
import numpy as np
import time

print('Starting camera sender...')

def run_camera(input_str, address, port, protocol, pattern=0, fps=25, send_rate=25, client_plugins={}):
    """Runs the camera, sends messages
    Args:
        input_str (str): Path to video file **OR** an `int` for camera input
        address (str): URL of `OpenCV` server 
        port (int): Port of `OpenCV` server
        protocol (str): Protocol of of `OpenCV` server 
        pattern (int, optional): ZMQ Pattern. 0=`zmq.PAIR`, 1=`zmq.REQ/zmq.REP`; 2=`zmq.PUB,zmq.SUB`. Defaults to 0.
        fps (int, optional): Framerate for video capture. Defaults to 25.
    """
    if input_str.isdigit():
        input = int(input_str)
    else:
        input = input_str

    options = {'THREADED_QUEUE_MODE': False}
    if address == '':
        address = None
    # Open any video stream; `framerate` here is just for picamera
    stream = VideoGear(source=input, framerate=fps, **options).start()
    # server = NetGear() # Locally
    netgear_options = {'max_retries': 10, 'request_timeout': 10}
    server = NetGear(address=address, port=port, protocol=protocol,
                     pattern=pattern, receive_mode=False, logging=True, **netgear_options)

    _prev_frame = None
    while True:
        # Sleep
        time.sleep(1.0/send_rate)

        try:
            frame = stream.read()
            # check if frame is None
            if frame is None:
                print("Error: frame not found")
                break

            _prev_frame = frame 

            # send frame to server
            print('Debug: sending frame')
            server.send(frame)

        except KeyboardInterrupt:
            # break the infinite loop
            break

    # safely close video stream
    stream.stop()

# Send the camera frames to the specified server address over a tcp connection
run_camera('0', '192.168.0.2', '5454', 'tcp', 1)