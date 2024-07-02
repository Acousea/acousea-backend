from pydantic import BaseModel

from core.communication_system.domain.communicator.communication_result import CommunicationResult, CommunicationStatus
from core.iclisten.application.ports.iclisten_client import ICListenClient
from core.iclisten.domain.iclisten_device_info_read_model import ICListenDeviceInfoReadModel
from core.iclisten.infrastructure.sqlite_iclisten_repository import SQLiteICListenRepository
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class UpdateICListenDeviceInfoQueryParams(BaseModel):
    ip: str


class UpdateICListenDeviceInfoRequestResult(BaseModel):
    status: str
    message: str


class UpdateICListenDeviceInfoHttpRequest(HttpRequest[UpdateICListenDeviceInfoQueryParams, UpdateICListenDeviceInfoRequestResult]):
    def __init__(self, client: ICListenClient):
        self.iclisten_client = client

    def execute(self, params: UpdateICListenDeviceInfoQueryParams | None = None) -> HttpResponse[UpdateICListenDeviceInfoRequestResult]:
        if params is None:
            return HttpResponse.fail(message="You need to specify an ip")
        result = self.iclisten_client.update_device_info()
        if result.status == CommunicationStatus.SUCCESS:
            return HttpResponse.ok(
                UpdateICListenDeviceInfoRequestResult(
                    status=result.status,
                    message=result.message
                )
            )
        return HttpResponse.fail(message=result.message, code=result.error_code)

