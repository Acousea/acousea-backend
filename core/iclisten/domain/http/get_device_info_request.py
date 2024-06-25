from pydantic import BaseModel

from core.iclisten.domain.device_info_read_model import DeviceInfoReadModel
from core.iclisten.infrastructure.iclisten_request_handler import ICListenRequestHandler
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetDeviceInfoQueryParams(BaseModel):
    ip: str


class GetDeviceInfoHttpRequest(HttpRequest[GetDeviceInfoQueryParams, DeviceInfoReadModel]):
    def __init__(self, request_handler: ICListenRequestHandler):
        self.request_handler = request_handler

    def execute(self, params: GetDeviceInfoQueryParams | None = None) -> HttpResponse[DeviceInfoReadModel]:
        if params is None:
            return HttpResponse.fail(message="You need to specify an ip")
        return HttpResponse.ok(self.request_handler.retrieve_device_info())
