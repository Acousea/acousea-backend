from pydantic import BaseModel

from data_backend.device.info.application.ports.device_info_query_repository import DeviceInfoQueryRepository
from data_backend.device.info.domain.device_info_read_model import DeviceInfoReadModel
from data_backend.shared.application.httprequest import HttpRequest
from data_backend.shared.domain.httpresponse import HttpResponse


class GetDeviceInfoQueryParams(BaseModel):
    ip: str


class GetDeviceInfoHttpRequest(HttpRequest[GetDeviceInfoQueryParams, DeviceInfoReadModel]):
    def __init__(self, query_repository: DeviceInfoQueryRepository):
        self.query_repository = query_repository

    def execute(self, params: GetDeviceInfoQueryParams | None = None) -> HttpResponse[DeviceInfoReadModel]:
        if params is None:
            return HttpResponse.fail(message="You need to specify an ip")
        return HttpResponse.ok(self.query_repository.get_all())
