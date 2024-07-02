from pydantic import BaseModel

from core.iclisten.domain.iclisten_device_info_read_model import ICListenDeviceInfoReadModel
from core.iclisten.infrastructure.sqlite_iclisten_repository import SQLiteICListenRepository
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetDeviceInfoQueryParams(BaseModel):
    ip: str


class GetDeviceInfoHttpRequest(HttpRequest[GetDeviceInfoQueryParams, ICListenDeviceInfoReadModel]):
    def __init__(self, repository: SQLiteICListenRepository):
        self.repository = repository

    def execute(self, params: GetDeviceInfoQueryParams | None = None) -> HttpResponse[ICListenDeviceInfoReadModel]:
        if params is None:
            return HttpResponse.fail(message="You need to specify an ip")
        return HttpResponse.ok(self.repository.get_device_info())
