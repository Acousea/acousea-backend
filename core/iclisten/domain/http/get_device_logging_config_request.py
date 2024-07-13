from core.communication_system.domain.communicator.communication_result import CommunicationStatus, CommunicationResultHttpResponse
from core.iclisten.application.ports.iclisten_client import PAMDeviceClient

from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetPAMDeviceLoggingConfigHttpRequest(HttpRequest[None, CommunicationResultHttpResponse]):
    def __init__(self, pam_device_client: PAMDeviceClient):
        self.pam_device_client = pam_device_client

    def execute(self, params: None = None) -> HttpResponse[CommunicationResultHttpResponse]:
        result = self.pam_device_client.update_logging_config()
        if result.status == CommunicationStatus.SUCCESS:
            return HttpResponse.ok(
                CommunicationResultHttpResponse(
                    status=result.status,
                    message=result.message
                )
            )
        return HttpResponse.fail(message=result.message, code=result.error_code)
