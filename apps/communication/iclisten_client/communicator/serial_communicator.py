import serial

from apps.communication.communication_requests.communication_request import CommunicationRequest
from apps.communication.communication_responses.communication_response import CommunicationResponse
from apps.communication.iclisten_client.communicator.communicator import Communicator


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

    def send_request(self, request: CommunicationRequest) -> CommunicationResponse:
        if self.serial is None:
            self.init(self.baud_rate, self.device, self.timeout)
        print("Command (as bytes):", request.encode())
        self.serial.write(request.encode())
        self.serial.flush()
        response = CommunicationResponse(self.serial.readline())
        print("Response: ", response)
        return response

    def close(self):
        if self.serial is not None:
            self.serial.close()
