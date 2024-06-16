from typing import Type

import serial

from apps.communication.communication_requests.communication_request import CommunicationRequest
from apps.communication.communication_responses.communication_response import CommunicationResponse
from apps.communication.communicator.communicator import Communicator


# FIXME: Must become async
class SerialCommunicator(Communicator):
    def __init__(self, device, baud_rate: int = 9600, timeout: float = 3.0):
        self.serial = None
        self.device = device
        self.baud_rate = baud_rate
        self.timeout = timeout

    def init(self, baud_rate, device, timeout):
        self.serial = serial.Serial(device,
                                    baudrate=baud_rate,
                                    timeout=timeout,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS
                                    )

    def send_request(self, request: CommunicationRequest,
                     response_cls: Type[CommunicationResponse]) -> CommunicationResponse:
        if self.serial is None:
            self.init(self.baud_rate, self.device, self.timeout)
        print("Command (as bytes):", request.encode())
        self.serial.write(request.encode())
        self.serial.flush()
        header = self.serial.read(3)
        if header[0] != 0x20:
            raise ValueError("Invalid sync byte header: Expected 0x20, Actual: 0x{:02x}".format(header[0]))
        response_length = header[2]
        response_bytes = header + self.serial.read(response_length + 1)
        response = response_cls(response_bytes)
        return response

    def close(self):
        if self.serial is not None:
            self.serial.close()
