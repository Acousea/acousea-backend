import random
import struct

from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.shared.domain.address import Address, RequestType
from core.shared.domain.operation_codes import OperationCode


class CommunicationRequestMother:
    @staticmethod
    def create() -> CommunicationRequest:
        request = CommunicationRequestMother._generate_fake_response()
        print("response: ", ''.join(f"{byte:02x}" for byte in request))
        return CommunicationRequest.reconstruct_from_bytes(request)

    @staticmethod
    def _generate_fake_response() -> bytes:
        sync_byte = 0x20
        opcode = OperationCode.to_int(OperationCode.GET_PAM_DEVICE_INFO)
        addresses: bytes = Address.BACKEND << 6 | Address.PI3 << 4 | RequestType.LORA_PACKET
        data_length = ord(bytes([int(10)]))
        # Generate 10 random bytes
        payload = bytes([random.randint(0, 255) for _ in range(10)])

        response_content = struct.pack(
            '<BBBB10s',
            sync_byte,  # 1 byte (B)
            opcode,  # 1 byte (B)
            addresses,  # 1 byte (B)
            data_length,  # 1 byte (B)
            payload  # 10 bytes (10s)
        )

        return response_content


if __name__ == "__main__":
    fake_request = CommunicationRequestMother.create()
    print(fake_request)
    print(fake_request.op_code)
    print(fake_request.sender_address)
    print(fake_request.recipient_address)
    print(fake_request.request_type)

