from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.iclisten.domain.pam_system_logging_config_read_model import PAMDeviceFFTLoggingConfig, \
    PAMDeviceWaveformLoggingConfig
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class SetDeviceLoggingConfigRequest(CommunicationRequest):

    def __init__(self, wav_config: PAMDeviceWaveformLoggingConfig, fft_config: PAMDeviceFFTLoggingConfig):
        payload = self.encode_payload(wav_config, fft_config)
        super().__init__(OperationCode.SET_PAM_DEVICE_LOGGING_CONFIG, Address.PI3, payload)

    @staticmethod
    def encode_payload(wav_config: PAMDeviceWaveformLoggingConfig, fft_config: PAMDeviceFFTLoggingConfig) -> bytes:
        # Waveform Configuration
        gain = wav_config.gain.to_bytes(2, 'little')
        waveform_sample_rate = wav_config.sample_rate.to_bytes(4, 'little')
        waveform_logging_mode = wav_config.logging_mode.to_bytes(1, 'little')
        waveform_log_length = wav_config.log_length.to_bytes(1, 'little')
        data_format = SetDeviceLoggingConfigRequest.map_bit_depth(wav_config.bit_depth).to_bytes(1, 'little')

        # FFT Configuration
        fft_sample_rate = fft_config.sample_rate.to_bytes(4, 'little')
        fft_processing_type = fft_config.fft_processing_type.to_bytes(2, 'little')
        ffts_accumulated = fft_config.ffts_accumulated.to_bytes(2, 'little')
        fft_logging_mode = fft_config.logging_mode.to_bytes(1, 'little')
        fft_log_length = fft_config.log_length.to_bytes(1, 'little')

        payload = bytearray()
        payload.extend(gain)
        payload.extend(waveform_sample_rate)
        payload.append(waveform_logging_mode[0])
        payload.append(waveform_log_length[0])
        payload.append(data_format[0])
        payload.extend(fft_sample_rate)
        payload.extend(fft_processing_type)
        payload.extend(ffts_accumulated)
        payload.append(fft_logging_mode[0])
        payload.append(fft_log_length[0])

        return bytes(payload)

    @staticmethod
    def map_bit_depth(bit_depth: int) -> int:
        bit_depth_map = {
            2: 16,
            3: 24,
            4: 32
        }
        return bit_depth_map.get(bit_depth, 16)

    def __str__(self):
        return f'SetDeviceLoggingConfigRequest{super().__str__()}'

    def __repr__(self):
        return f'SetDeviceLoggingConfigRequest{super().__repr__()}'
