import socket
import sys
import threading
import time
import toml

SEND_RATE = 4

class DetectionServer:
    def __init__(self):
        config = toml.load('../Config.toml')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(0.1)

        print('Detection Server: Socket created')

        #Bind socket to local host and port
        try:
            port = int(config['edge_server']['detection']['port'])
            self.sock.bind(('', port))
        except socket.error as msg:
            print('Detection Server: Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
            
        print('Detection Server: Socket bind complete')

        #Start listening on socket
        self.sock.listen(10)
        print(f'Detection Server: Socket now listening on 0.0.0.0:{port}')

        self.stopped = False
    
        t = threading.Thread(target=self.start_listening)
        t.start()
        self.listen_thread = t
        self.client_thread = None
        self.client_conn = None
        
        self.last_message = None


    def start_listening(self):
        while not self.stopped:
            try:
                (conn, addr) = self.sock.accept()
                print('Client connected with ' + addr[0] + ':' + str(addr[1]))
                t = threading.Thread(target=self.client_connection)
                t.start()
                self.client_thread = t
                self.client_conn = conn
                self.client_addr = addr
                break
            except socket.timeout:
                # print("Socket time out")
                pass


    def client_connection(self):
        while not self.stopped:
            if self.last_message is not None:
                message = bytes(self.last_message, 'ascii')
                self.client_conn.sendall(message)
                print(f'Forwarded message to client \'{message}\'')
            time.sleep(1.0/SEND_RATE)


    def send_detection(self, class_id, x_loc):
        self.last_message = str(class_id) + ',' + str(x_loc)


    def stop(self):
        self.stopped = True
        self.listen_thread.join()
        if self.client_thread is not None:
            self.client_thread.join()
        self.sock.close()
