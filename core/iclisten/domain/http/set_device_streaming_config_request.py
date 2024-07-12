from typing import Optional

from pydantic import BaseModel

from core.communication_system.domain.communicator.communication_result import CommunicationStatus, CommunicationResultHttpResponse
from core.iclisten.application.ports.iclisten_client import PAMDeviceClient
from core.iclisten.domain.pam_system_streaming_config_read_model import PAMDeviceWaveformStreamingConfig, PAMDeviceFFTStreamingConfig
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


# Definición de los query parameters para la request
class SetPAMDeviceStreamingConfigRequestParams(BaseModel):
    wav_config: PAMDeviceWaveformStreamingConfig
    fft_config: PAMDeviceFFTStreamingConfig


# Request para actualizar la configuración de streaming
class SetDeviceStreamingConfigHttpRequest(HttpRequest[SetPAMDeviceStreamingConfigRequestParams, CommunicationResultHttpResponse]):
    def __init__(self, pam_device_client: 'PAMDeviceClient'):
        self.pam_device_client = pam_device_client

    def execute(self, params: Optional[SetPAMDeviceStreamingConfigRequestParams] = None) -> HttpResponse[CommunicationResultHttpResponse]:
        if not params:
            raise ValueError("Missing required parameters")
        # Print the params
        print("PARAMS:", params)

        result = self.pam_device_client.set_streaming_config(params.wav_config, params.fft_config)
        if result.status == CommunicationStatus.SUCCESS:
            return HttpResponse.ok(
                CommunicationResultHttpResponse(
                    status=result.status,
                    message=result.message
                )
            )
        return HttpResponse.fail(message=result.message, code=result.error_code)
