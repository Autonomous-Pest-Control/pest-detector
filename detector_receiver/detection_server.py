import socket
import sys
import threading

HOST = ''	# Symbolic name meaning all available interfaces
PORT = 5455	# Arbitrary non-privileged port

class DetectionServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(0.1)

        print('Socket created')

        #Bind socket to local host and port
        try:
            self.sock.bind((HOST, PORT))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
            
        print('Socket bind complete')

        #Start listening on socket
        self.sock.listen(10)
        print('Socket now listening')

        self.stopped = False
    
        t = threading.Thread(target=self.start_listening)
        t.start()
        self.listen_thread = t
        self.client_thread = None
        self.conn = None

    def start_listening(self):
        while not self.stopped:
            try:
                (conn, addr) = self.sock.accept()
                print('Client connected with ' + addr[0] + ':' + str(addr[1]))
                t = threading.Thread(target=self.client_connection)
                t.start()
                self.client_thread = t
                break
            except socket.timeout:
                # print("Socket time out")
                pass


    def client_connection(self):
        while not self.stopped:
            print('Client connection')


    def stop(self):
        self.stopped = True
        self.listen_thread.join()
        if self.client_thread is not None:
            self.client_thread.join()
        self.sock.close()
