#!/usr/bin/env python3
import serial
import time
import threading
import time
import toml
import sys
import struct


SEND_RATE = 20
MESSAGE_SIZE = 2
STATUS_READY = 1

class Controller:
    def __init__(self):
        self.last_message = None
        self.uart_thread = None
        self.stopped = False

        config = toml.load('../Config.toml')
        self.device = config['serial']['device_name']
        ser = serial.Serial(self.device, 9600, timeout=1)
        ser.reset_input_buffer()
        self.ser = ser

        # Create the main thread
        t = threading.Thread(target=self.start_uart)
        t.start()
        self.uart_thread = t


    def start_uart(self):
        while not self.stopped:
            try:
                read_message = self.ser.read(MESSAGE_SIZE)
                read_bytes = list(read_message)

                status = read_bytes[0]
                debug_info = read_bytes[1]
                print(f'From arduino: STATUS="{status}", INFO="{debug_info}"')


                if status == STATUS_READY and self.last_message is not None:
                    self.ser.write(self.serialize_message())
                    self.last_message = None
                time.sleep(1.0/SEND_RATE)
            except serial.SerialException:
                print("Error: serial error. Terminating")
                break


    def serialize_message(self):
        buffer = bytes([self.last_message[0]])
        buffer += bytes([self.last_message[1]])
        return bytearray(buffer)


    def send_command(self, cmd_id, cmd_arg):
        self.last_message = (cmd_id, cmd_arg)


    def stop(self):
        self.stopped = True
        self.uart_thread.join()
        if self.uart_thread is not None:
            self.uart_thread.join()
        self.sock.close()
