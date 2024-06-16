from apps.communication.communication_responses.communication_response import CommunicationResponse
import struct


class GetDeviceInfoResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        response_content = super().content()

        # Decodificación de la respuesta según el formato descrito
        self.unit_status = response_content[0]
        self.battery_status = response_content[1]

        self.unit_time = int.from_bytes(response_content[2:6], 'little')
        self.time_sync = response_content[6]

        self.temperature = self._bytes_to_float(response_content[7:11])
        self.humidity = self._bytes_to_float(response_content[11:15])
        self.hydrophone_sensitivity = self._bytes_to_float(response_content[15:19])

        self.record_wav = response_content[19]
        self.waveform_sample_rate = int.from_bytes(response_content[20:24], 'little')

        self.record_fft = response_content[24]
        self.fft_sample_rate = int.from_bytes(response_content[25:29], 'little')

        # Asumir que el firmware y hardware release son cadenas de longitud fija y contienen solo caracteres imprimibles
        self.firmware_release = response_content[29:37].decode('ascii', 'ignore').strip('\x00')
        self.hardware_release = response_content[37:45].decode('ascii', 'ignore').strip('\x00')

        # IP address as a string
        self.ip_address = '.'.join(str(b) for b in response_content[45:49])

    def _bytes_to_float(self, bytes_seq):
        return struct.unpack('f', bytes_seq)[0]

    def __str__(self):
        return (f"GetDeviceInfoResponse(unit_status={self.unit_status}, battery_status={self.battery_status},"
                f" unit_time={self.unit_time}, time_sync={self.time_sync}, temperature={self.temperature},"
                f" humidity={self.humidity}, hydrophone_sensitivity={self.hydrophone_sensitivity}, "
                f"record_wav={self.record_wav}, waveform_sample_rate={self.waveform_sample_rate}, "
                f"record_fft={self.record_fft}, fft_sample_rate={self.fft_sample_rate}, firmware_release={self.firmware_release},"
                f" hardware_release={self.hardware_release}, ip_address={self.ip_address})")
