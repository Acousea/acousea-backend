from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class PAMDeviceLoggingConfigCommunicationResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        response_content = self.data

        # Asegúrate de que la longitud del contenido de la respuesta es correcta
        if len(response_content) < 19:
            raise ValueError("Invalid response length. Response content size=" + str(len(response_content)))

        # Waveform configuration
        self.gain = int.from_bytes(response_content[0:2], 'little')
        self.waveform_sample_rate = int.from_bytes(response_content[2:6], 'little')
        self.waveform_logging_mode = response_content[6]
        self.waveform_log_length = response_content[7]
        self.bit_depth = response_content[8]

        # FFT configuration
        self.fft_sample_rate = int.from_bytes(response_content[9:13], 'little')
        self.fft_processing_type = int.from_bytes(response_content[13:15], 'little')
        self.ffts_accumulated = int.from_bytes(response_content[15:17], 'little')
        self.fft_logging_mode = response_content[17]
        self.fft_log_length = response_content[18]

    def __str__(self):
        return (f"PAMDeviceLoggingConfigCommunicationResponse(waveform_sample_rate={self.waveform_sample_rate}, gain={self.gain}, "
                f"waveform_logging_mode={self.waveform_logging_mode}, waveform_log_length={self.waveform_log_length}, bit_depth={self.bit_depth}, "
                f"fft_sample_rate={self.fft_sample_rate}, fft_processing_type={self.fft_processing_type}, ffts_accumulated={self.ffts_accumulated}, "
                f"fft_logging_mode={self.fft_logging_mode}, fft_log_length={self.fft_log_length})")
