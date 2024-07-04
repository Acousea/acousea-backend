import random
import struct
from datetime import datetime

from core.communication_system.domain.communicator.responses.drifter_simple_report_response import DrifterSimpleReportResponse
from core.communication_system.domain.communicator.responses.localizer_simple_report_response import \
    LocalizerSimpleReportResponse
from core.shared.domain.address import Address, RequestType
from core.shared.domain.operation_codes import OperationCode


class LocalizerDrifterSimpleReportResponseMother:
    @staticmethod
    def create_localizer_simple_report_response() -> LocalizerSimpleReportResponse:
        response = LocalizerDrifterSimpleReportResponseMother._generate_fake_response(drifter=False)
        print("response: ", ''.join(f"{byte:02x}" for byte in response))
        return LocalizerSimpleReportResponse(response)

    @staticmethod
    def create_drifter_simple_report_response() -> DrifterSimpleReportResponse:
        response = LocalizerDrifterSimpleReportResponseMother._generate_fake_response(drifter=True)
        print("response: ", ''.join(f"{byte:02x}" for byte in response))
        return DrifterSimpleReportResponse(response)

    @staticmethod
    def _generate_fake_response(drifter: bool = False) -> bytes:
        sync_byte = 0x20
        opcode = OperationCode.to_int(OperationCode.SUMMARY_SIMPLE_REPORT)

        addresses: bytes = b''
        if drifter:
            addresses: bytes = Address.DRIFTER << 6 | Address.BACKEND << 4 | RequestType.LORA_PACKET  # addresses = SENDER_ADDRESS << 6 | RECIPIENT_ADDRESS << 4 | ADDRESS_TYPE
        else:
            addresses: bytes = Address.LOCALIZER << 6 | Address.BACKEND << 4 | RequestType.LORA_PACKET
        data_length = ord(bytes([int(14)]))

        epoch_time = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())
        battery_percent = ord(bytes([random.randint(0, 100)]))
        latitude = float(random.uniform(-90.0, 90.0))
        longitude = float(random.uniform(-180.0, 180.0))
        operation_mode = ord(bytes([random.randint(0, 3)]))

        print("Sync byte: ", sync_byte)
        print("opcode: ", opcode)
        print("addresses: ", addresses)
        print("data_length: ", data_length)

        print("epoch_time: ", epoch_time)
        print("battery_percent: ", battery_percent)
        print("latitude: ", latitude)
        print("longitude: ", longitude)
        print("operation_mode: ", operation_mode)

        response_content = struct.pack(
            '<BBBBIBffB',
            sync_byte,  # 1 byte (B)
            opcode,  # 1 byte (B)
            addresses,  # 1 byte (B)
            data_length,  # 1 byte (B)
            epoch_time,  # 4 bytes (I)
            battery_percent,  # 1 byte (B)
            latitude,  # 4 bytes (f)
            longitude,  # 4 bytes (f)
            operation_mode  # 1 byte (B)
        )

        return response_content


if __name__ == "__main__":
    fake_localizer_response = LocalizerDrifterSimpleReportResponseMother.create_localizer_simple_report_response()
    fake_drifter_response = LocalizerDrifterSimpleReportResponseMother.create_drifter_simple_report_response()

    print(fake_localizer_response)
    print(fake_drifter_response)
