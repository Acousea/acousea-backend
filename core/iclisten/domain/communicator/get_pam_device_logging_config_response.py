import datetime

from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class GetPAMDeviceLoggingConfigCommunicationResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        response_content = super().content()

        # Waveform configuration
        self.log_waveform = bool(response_content[0])
        self.gain = int.from_bytes(response_content[1:3], 'little')
        self.waveform_sample_rate = int.from_bytes(response_content[3:7], 'little')
        self.waveform_logging_mode = response_content[7]
        self.waveform_log_length = response_content[8]
        self.data_format = response_content[9]

        # FFT configuration
        self.log_fft = bool(response_content[10])
        self.reference_level = int.from_bytes(response_content[11:13], 'little')
        self.fft_sample_rate = int.from_bytes(response_content[13:17], 'little')
        self.points_per_fft = int.from_bytes(response_content[17:19], 'little')
        self.fft_processing_type = int.from_bytes(response_content[19:21], 'little')
        self.samples_between_ffts = int.from_bytes(response_content[21:23], 'little')
        self.ffts_accumulated = int.from_bytes(response_content[23:25], 'little')
        self.fft_weighting_factor = int.from_bytes(response_content[25:27], 'little')
        self.fft_logging_mode = response_content[27]
        self.fft_log_length = response_content[28]

        self.timestamp = self.get_date_from_unix_timestamp(int.from_bytes(response_content[29:33], 'little'))

    @staticmethod
    def get_date_from_unix_timestamp(timestamp: int) -> str:
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return (f"GetPAMDeviceLoggingConfigCommunicationResponse(log_waveform={self.log_waveform}, gain={self.gain}, "
                f"waveform_sample_rate={self.waveform_sample_rate}, waveform_logging_mode={self.waveform_logging_mode}, "
                f"waveform_log_length={self.waveform_log_length}, data_format={self.data_format}, log_fft={self.log_fft}, "
                f"reference_level={self.reference_level}, fft_sample_rate={self.fft_sample_rate}, points_per_fft={self.points_per_fft}, "
                f"fft_processing_type={self.fft_processing_type}, samples_between_ffts={self.samples_between_ffts}, "
                f"ffts_accumulated={self.ffts_accumulated}, fft_weighting_factor={self.fft_weighting_factor}, "
                f"fft_logging_mode={self.fft_logging_mode}, fft_log_length={self.fft_log_length}, timestamp={self.timestamp})")
