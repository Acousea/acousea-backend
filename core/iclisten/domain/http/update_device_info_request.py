from pydantic import BaseModel

from core.communication_system.domain.communicator.communication_result import CommunicationStatus, CommunicationResultHttpResponse
from core.iclisten.application.ports.iclisten_client import PAMDeviceClient
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class UpdateICListenDeviceInfoQueryParams(BaseModel):
    ip: str


class UpdateICListenDeviceInfoHttpRequest(HttpRequest[UpdateICListenDeviceInfoQueryParams, CommunicationResultHttpResponse]):
    def __init__(self, client: PAMDeviceClient):
        self.iclisten_client = client

    def execute(self, params: UpdateICListenDeviceInfoQueryParams | None = None) -> HttpResponse[CommunicationResultHttpResponse]:
        if params is None:
            return HttpResponse.fail(message="You need to specify an ip")
        result = self.iclisten_client.update_device_info()
        if result.status == CommunicationStatus.SUCCESS:
            return HttpResponse.ok(
                CommunicationResultHttpResponse(
                    status=result.status,
                    message=result.message
                )
            )
        return HttpResponse.fail(message=result.message, code=result.error_code)

