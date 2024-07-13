from core.communication_system.domain.communicator.communication_result import CommunicationResult
from core.communication_system.infrastructure.communicator.communicator_service import CommunicatorService
from core.iclisten.domain.communicator.get_pam_device_info_request import GetDeviceInfoRequest
from core.iclisten.domain.communicator.get_pam_device_logging_config_request import GetDeviceLoggingConfigRequest
from core.iclisten.domain.communicator.get_pam_device_streaming_config_request import GetDeviceStreamingConfigRequest
from core.iclisten.domain.communicator.set_pam_device_logging_config_request import SetDeviceLoggingConfigRequest
from core.iclisten.domain.communicator.set_pam_device_streaming_config_request import SetDeviceStreamingConfigRequest
from core.iclisten.domain.pam_system_logging_config_read_model import PAMDeviceFFTLoggingConfig, PAMDeviceWaveformLoggingConfig
from core.iclisten.domain.pam_system_streaming_config_read_model import PAMDeviceFFTStreamingConfig, PAMDeviceWaveformStreamingConfig


class PAMDeviceClient:
    def __init__(self, communicator_service: CommunicatorService):
        self.communicator_service = communicator_service

    def update_device_info(self) -> CommunicationResult:
        result = self.communicator_service.send_request(GetDeviceInfoRequest())
        return result

    def update_streaming_config(self) -> CommunicationResult:
        result = self.communicator_service.send_request(GetDeviceStreamingConfigRequest())
        return result

    def set_streaming_config(self, wav_config: PAMDeviceWaveformStreamingConfig, fft_config: PAMDeviceFFTStreamingConfig) -> CommunicationResult:
        request = SetDeviceStreamingConfigRequest(wav_config, fft_config)
        return self.communicator_service.send_request(request)

    def set_logging_config(self, wav_config: PAMDeviceWaveformLoggingConfig, fft_config: PAMDeviceFFTLoggingConfig) -> CommunicationResult:
        request = SetDeviceLoggingConfigRequest(wav_config, fft_config)
        return self.communicator_service.send_request(request)

    def update_logging_config(self) -> CommunicationResult:
        result = self.communicator_service.send_request(GetDeviceLoggingConfigRequest())
        return result
