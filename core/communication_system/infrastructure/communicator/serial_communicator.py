import serial

from core.communication_system.application.ports.communicator import Communicator
from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.communication_system.domain.communicator.responses.error_response import ErrorCommunicationResponse
from core.shared.domain.address import Address

from core.shared.domain.operation_codes import OperationCode


# FIXME: Must become async
class SerialCommunicator(Communicator):
    def __init__(self, device, baud_rate: int = 9600, timeout: float = 4.0):
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

    def send_custom_request(self) -> bytes:
        if self.serial is None:
            self.init(self.baud_rate, self.device, self.timeout)

        addresses: int = (Address.BACKEND << 6) | (Address.PI3 << 4) | Address.LORA_PACKET  # FROM: BACKEND TO: ?
        request = b'\x20' + bytes([ord('0')]) + bytes([addresses]) + b'\x04' + b'\x00\xFF\x00\xFF'
        print("Fake Encoded request:", ' '.join(f'{byte:02x}' for byte in request))
        self.serial.write(request)
        self.serial.flush()
        # FIXME: Might need to add a delay here
        header = self.serial.read(4)
        if header is None:
            raise ValueError("No response header received")
        if len(header) < 4:
            raise ValueError("Invalid response header: Expected 4 bytes, Actual: {}".format(len(header)))
        if header[0] != 0x20:
            raise ValueError("Invalid sync byte header: Expected 0x20, Actual: 0x{:02x}".format(header[0]))

        response_length = header[3]
        response_packet = header + self.serial.read(response_length + 1)

        op_code = header[1]
        if op_code == OperationCode.to_int(OperationCode.ERROR):
            error = ErrorCommunicationResponse(response_packet)
            raise ValueError("Error response received: {}".format(error))

        # Imprimir RESPONSE PACKET como bytes en hexadecimal
        response_hex = ' '.join(f'{byte:02x}' for byte in response_packet)
        print("RESPONSE PACKET (HEX):", response_hex)
        return response_packet


    def send_request(self, request: CommunicationRequest) -> bytes:
        if self.serial is None:
            self.init(self.baud_rate, self.device, self.timeout)
        print("Command (as bytes):", request)
        self.serial.write(request.encode())
        self.serial.flush()
        # FIXME: Might need to add a delay here
        header = self.serial.read(4)
        if header is None:
            raise ValueError("No response header received")
        if len(header) < 4:
            raise ValueError("Invalid response header: Expected 4 bytes, Actual: {}".format(len(header)))
        if header[0] != 0x20:
            raise ValueError("Invalid sync byte header: Expected 0x20, Actual: 0x{:02x}".format(header[0]))

        response_length = header[3]
        response_packet = header + self.serial.read(response_length + 1)

        op_code = header[1]
        if op_code == OperationCode.to_int(OperationCode.ERROR):
            error = ErrorCommunicationResponse(response_packet)
            raise ValueError("Error response received: {}".format(error))

        # Imprimir RESPONSE PACKET como bytes en hexadecimal
        response_hex = ' '.join(f'{byte:02x}' for byte in response_packet)
        print("RESPONSE PACKET (HEX):", response_hex)
        return response_packet

    def close(self):
        if self.serial is not None:
            self.serial.close()


if __name__ == "__main__":
    communicator = SerialCommunicator("COM3")
    communicator.send_custom_request()
    communicator.close()