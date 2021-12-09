import socket
import sys
import threading
import time
import struct
import toml

SEND_RATE = 4

class DetectionServer:
    def __init__(self):
        self.client_conn = None
        self.last_message = None
        self.client_thread = None
        self.stopped = False

        config = toml.load('../Config.toml')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(0.1)
        print('Detection Server: Socket created')

        # Bind socket to local host and port
        try:
            port = int(config['edge_server']['detection']['port'])
            self.sock.bind(('', port))
            print('Detection Server: Socket bind complete')
        except socket.error as msg:
            print('Detection Server: Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
            
        # Start listening on socket
        self.sock.listen(10)
        print(f'Detection Server: listening on 0.0.0.0:{port}')

        # Create the main server listening thread
        t = threading.Thread(target=self.start_listening)
        t.start()
        self.listen_thread = t


    def start_listening(self):
        while not self.stopped:
            # Only accept 1 client connection
            if self.client_conn is not None:
                continue
            try:
                (conn, addr) = self.sock.accept()
                print('Detection Server: client connected with ' + addr[0] + ':' + str(addr[1]))
                self.client_conn = conn
                t = threading.Thread(target=self.client_connection)
                self.client_thread = t
                t.start()
            except socket.timeout:
                pass


    def serialize_message(self):
        print(f"serialize message=({self.last_message[0]},{self.last_message[1]})")
        buffer = bytes([self.last_message[0]])
        buffer += struct.pack('f', self.last_message[1])

        print(f"generated len({len(buffer)}) buf={buffer}")
        return bytearray(buffer)


    def client_connection(self):
        while not self.stopped:
            try:
                if self.last_message is not None:
                    message = self.serialize_message()
                    self.client_conn.sendall(message)
                    self.last_message = None
                    # print(f'Forwarded message to client \'{message}\'')
                time.sleep(1.0/SEND_RATE)
            except socket.error:
                e = sys.exc_info()[1]
                print(f'Detection Server: socket error={e}. Terminating...')
                break
        self.client_conn = None


    def send_detection(self, class_id, x_loc):
        self.last_message = (class_id,x_loc)


    def stop(self):
        self.stopped = True
        self.listen_thread.join()
        if self.client_thread is not None:
            self.client_thread.join()
        self.sock.close()
