import datetime
import struct
from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class GetPAMDeviceStreamingConfigCommunicationResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        response_content = super().content()

        # Decodificación de la respuesta según el formato descrito
        self.record_waveform = bool(response_content[0])
        self.process_waveform = bool(response_content[1])
        self.waveform_processing_type = response_content[2]
        self.waveform_interval = int.from_bytes(response_content[3:7], 'little')
        self.waveform_duration = int.from_bytes(response_content[7:11], 'little')

        self.record_fft = bool(response_content[11])
        self.process_fft = bool(response_content[12])
        self.fft_processing_type = response_content[13]
        self.fft_interval = int.from_bytes(response_content[14:18], 'little')
        self.fft_duration = int.from_bytes(response_content[18:22], 'little')

        self.timestamp = self.get_date_from_unix_timestamp(int.from_bytes(response_content[22:26], 'little'))

    @staticmethod
    def _bytes_to_float(bytes_seq: bytes):
        return struct.unpack('f', bytes_seq)[0]

    @staticmethod
    def get_date_from_unix_timestamp(timestamp: int) -> str:
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return (f"GetPAMDeviceStreamingConfigCommunicationResponse(record_waveform={self.record_waveform},"
                f" process_waveform={self.process_waveform}, waveform_processing_type={self.waveform_processing_type},"
                f" waveform_interval={self.waveform_interval}, waveform_duration={self.waveform_duration},"
                f" record_fft={self.record_fft}, process_fft={self.process_fft}, fft_processing_type={self.fft_processing_type},"
                f" fft_interval={self.fft_interval}, fft_duration={self.fft_duration}, timestamp={self.timestamp})")
