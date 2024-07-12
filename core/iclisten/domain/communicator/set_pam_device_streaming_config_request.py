from pydantic import BaseModel

from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.iclisten.domain.pam_system_streaming_config_read_model import PAMDeviceFFTStreamingConfig, PAMDeviceWaveformStreamingConfig
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class SetDeviceStreamingConfigRequest(CommunicationRequest):
    def __init__(self, wav_config: PAMDeviceWaveformStreamingConfig, fft_config: PAMDeviceFFTStreamingConfig):
        payload = self.encode_payload(wav_config, fft_config)
        super().__init__(OperationCode.SET_PAM_DEVICE_STREAMING_CONFIG, Address.PI3, payload)

    @staticmethod
    def encode_payload(wav_config: PAMDeviceWaveformStreamingConfig, fft_config: PAMDeviceFFTStreamingConfig) -> bytes:
        byte0 = ((wav_config.record_waveform & 0x01) << 3) | \
                ((fft_config.record_fft & 0x01) << 2) | \
                ((wav_config.process_waveform & 0x01) << 1) | \
                (fft_config.process_fft & 0x01)

        byte1 = ((wav_config.waveform_processing_type << 4) & 0xF0) | (fft_config.fft_processing_type & 0x0F)

        wav_period = wav_config.waveform_interval.to_bytes(2, 'little')
        wav_duration = wav_config.waveform_duration.to_bytes(2, 'little')
        fft_period = fft_config.fft_interval.to_bytes(2, 'little')
        fft_duration = fft_config.fft_duration.to_bytes(2, 'little')

        return bytes([byte0, byte1]) + wav_period + wav_duration + fft_period + fft_duration

    def __str__(self):
        return f'SetDeviceStreamingConfigRequest{super().__str__()}'

    def __repr__(self):
        return f'SetDeviceStreamingConfigRequest{super().__repr__()}'
