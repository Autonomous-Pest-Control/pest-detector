import socket
import sys
import threading

SERVER_ADDR = '192.168.0.2'	# Symbolic name meaning all available interfaces
PORT = 5455	# Arbitrary non-privileged port

class DeterrentClient:
    def __init__(self):
        pass 