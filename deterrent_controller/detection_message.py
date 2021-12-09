import struct

MESSAGE_LENGTH = 1 + 4

class DetectionMessage:
    def __init__(self, class_id, x_loc):
        self.class_id = class_id
        self.x_loc = x_loc

    @classmethod
    def from_bytes(cls, buffer):
        message = None
        if len(buffer) == MESSAGE_LENGTH:
            class_id = buffer[0]
            [x_loc] = struct.unpack('f', bytes(buffer[1:MESSAGE_LENGTH]))
            message = cls(class_id, x_loc)

        return message