from core.communication_system.domain.communicator.communication_result import CommunicationStatus, CommunicationResultHttpResponse
from core.iclisten.application.ports.iclisten_client import PAMDeviceClient
from core.iclisten.domain.pam_system_streaming_config_read_model import PAMDeviceStreamingConfigReadModel

from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetPAMDeviceStreamingConfigHttpRequest(HttpRequest[None, CommunicationResultHttpResponse]):
    def __init__(self, pam_device_client: PAMDeviceClient):
        self.pam_device_client = pam_device_client

    def execute(self, params: None = None) -> HttpResponse[PAMDeviceStreamingConfigReadModel]:
        result = self.pam_device_client.update_streaming_config()
        if result.status == CommunicationStatus.SUCCESS:
            return HttpResponse.ok(
                CommunicationResultHttpResponse(
                    status=result.status,
                    message=result.message
                )
            )
        return HttpResponse.fail(message=result.message, code=result.error_code)
