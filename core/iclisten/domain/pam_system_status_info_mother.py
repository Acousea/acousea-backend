import random
import struct
from datetime import datetime

from core.iclisten.domain.communicator.get_pam_device_info_response import GetPAMDeviceInfoCommunicationResponse
from core.shared.domain.address import Address, RequestType
from core.shared.domain.operation_codes import OperationCode


class PAMSystemStatusInfoMother:
    @staticmethod
    def create() -> GetPAMDeviceInfoCommunicationResponse:
        response = PAMSystemStatusInfoMother._generate_fake_response()
        print("response: ", ''.join(f"{byte:02x}" for byte in response))
        return GetPAMDeviceInfoCommunicationResponse(response)

    @staticmethod
    def _generate_fake_response() -> bytes:
        sync_byte = 0x20
        opcode = OperationCode.to_int(OperationCode.GET_PAM_DEVICE_INFO)
        addresses: bytes = Address.BACKEND << 6 | Address.PI3 << 4 | RequestType.LORA_PACKET
        data_length = ord(bytes([int(49)]))

        unit_status = ord(bytes([random.randint(0, 255)]))  # 1 byte (B)
        battery_status = ord(bytes([random.randint(0, 100)]))  # 1 byte (B)

        # # Generating a random unit_time (seconds since epoch)
        unit_time = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())  # 4 bytes (I)

        time_sync = ord(bytes([random.randint(0, 255)]))  # 1 byte (B)
        temperature = float(random.uniform(-40.0, 85.0))  # 4 bytes (f)
        humidity = float(random.uniform(0.0, 100.0))  # 4 bytes (f)
        hydrophone_sensitivity = float(random.uniform(-180.0, 180.0))  # 4 bytes (f)

        record_wav = ord(bytes([random.randint(0, 255)]))  # 1 byte (B)
        waveform_sample_rate = int(random.randint(0, 48000))  # 4 bytes (I)

        record_fft = ord(bytes([random.randint(0, 255)]))  # 1 byte (B)
        fft_sample_rate = int(random.randint(0, 48000))  # 4 bytes (I)

        firmware_release = "v1.0.0".ljust(8, '\x00').encode('ascii')  # 8 bytes (8s)
        hardware_release = "revA".ljust(8, '\x00').encode('ascii')  # 8 bytes (8s)

        ip_address = struct.pack('BBBB', random.randint(0, 255), random.randint(0, 255),
                                 random.randint(0, 255), random.randint(0, 255))  # 4 bytes (4s)

        print("unit_status: ", unit_status)
        print("battery_status: ", battery_status)
        print("unit_time: ", unit_time)
        print("time_sync: ", time_sync)
        print("temperature: ", temperature)
        print("humidity: ", humidity)
        print("hydrophone_sensitivity: ", hydrophone_sensitivity)
        print("record_wav: ", record_wav)
        print("waveform_sample_rate: ", waveform_sample_rate)
        print("record_fft: ", record_fft)
        print("fft_sample_rate: ", fft_sample_rate)
        print("firmware_release: ", firmware_release)
        print("hardware_release: ", hardware_release)
        print("ip_address: ", ip_address)

        response_content = struct.pack(
            '<BBBBBBIBfffBIBI8s8s4s',
            sync_byte,  # 1 byte (B)
            opcode,  # 1 byte (B)
            addresses,  # 1 byte (B)
            data_length,  # 1 byte (B)
            unit_status,  # 1 byte (B)
            battery_status,  # 1 byte (B)
            unit_time,  # 4 bytes (I)
            time_sync,  # 1 byte (B)
            temperature,  # 4 bytes (f)
            humidity,  # 4 bytes (f)
            hydrophone_sensitivity,  # 4 bytes (f)
            record_wav,  # 1 byte (B)
            waveform_sample_rate,  # 4 bytes (I)
            record_fft,  # 1 byte (B)
            fft_sample_rate,  # 4 bytes (I)
            firmware_release,  # 8 bytes (8s)
            hardware_release,  # 8 bytes (8s)
            ip_address  # 4 bytes (4s)
        )

        return response_content


if __name__ == "__main__":
    fake_response = PAMSystemStatusInfoMother.create()
    print(fake_response)
