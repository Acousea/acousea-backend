import datetime
import struct
from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class SetPAMDeviceStreamingConfigCommunicationResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        byte0 = self.data[0]
        byte1 = self.data[1]

        # Decodificación de los bits del byte0
        self.record_waveform = bool((byte0 >> 3) & 0x01)
        self.record_fft = bool((byte0 >> 2) & 0x01)
        self.process_waveform = bool((byte0 >> 1) & 0x01)
        self.process_fft = bool(byte0 & 0x01)

        # Decodificación de los bits del byte1
        self.waveform_processing_type = (byte1 >> 4) & 0x0F
        self.fft_processing_type = byte1 & 0x0F

        # Decodificación de los valores uint16_t
        self.waveform_interval = int.from_bytes(self.data[2:4], 'little')
        self.waveform_duration = int.from_bytes(self.data[4:6], 'little')
        self.fft_interval = int.from_bytes(self.data[6:8], 'little')
        self.fft_duration = int.from_bytes(self.data[8:10], 'little')

    def __str__(self):
        return (f"SetPAMDeviceStreamingConfigCommunicationResponse(record_waveform={self.record_waveform},"
                f" process_waveform={self.process_waveform}, waveform_processing_type={self.waveform_processing_type},"
                f" waveform_interval={self.waveform_interval}, waveform_duration={self.waveform_duration},"
                f" record_fft={self.record_fft}, process_fft={self.process_fft}, fft_processing_type={self.fft_processing_type},"
                f" fft_interval={self.fft_interval}, fft_duration={self.fft_duration})")
