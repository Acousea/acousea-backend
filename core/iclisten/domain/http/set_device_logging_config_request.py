from typing import Optional

from pydantic import BaseModel

from core.communication_system.domain.communicator.communication_result import CommunicationStatus, CommunicationResultHttpResponse
from core.iclisten.application.ports.iclisten_client import PAMDeviceClient
from core.iclisten.domain.pam_system_logging_config_read_model import PAMDeviceWaveformLoggingConfig, PAMDeviceFFTLoggingConfig
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class SetPAMDeviceLoggingConfigRequestParams(BaseModel):
    waveform_config: PAMDeviceWaveformLoggingConfig
    fft_config: PAMDeviceFFTLoggingConfig


# Request para actualizar la configuración de logging
class SetPAMDeviceLoggingConfigHttpRequest(HttpRequest[SetPAMDeviceLoggingConfigRequestParams, CommunicationResultHttpResponse]):
    def __init__(self, pam_device_client: PAMDeviceClient):
        self.pam_device_client = pam_device_client

    def execute(self, params: Optional[SetPAMDeviceLoggingConfigRequestParams] = None) -> HttpResponse[CommunicationResultHttpResponse]:
        if not params:
            raise ValueError("Missing required parameters")
        # Print the params
        print("PARAMS:", params)

        result = self.pam_device_client.set_logging_config(params.waveform_config, params.fft_config)
        if result.status == CommunicationStatus.SUCCESS:
            return HttpResponse.ok(
                CommunicationResultHttpResponse(
                    status=result.status,
                    message=result.message
                )
            )
        return HttpResponse.fail(message=result.message, code=result.error_code)
