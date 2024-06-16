from pydantic import BaseModel

from data_backend.iclisten.application.ports.iclisten_request_handler import ICListenRequestHandler
from data_backend.iclisten.domain.device_info_read_model import DeviceInfoReadModel
from data_backend.shared.application.httprequest import HttpRequest
from data_backend.shared.domain.httpresponse import HttpResponse


class GetDeviceInfoQueryParams(BaseModel):
    ip: str


class GetDeviceInfoHttpRequest(HttpRequest[GetDeviceInfoQueryParams, DeviceInfoReadModel]):
    def __init__(self, request_handler: ICListenRequestHandler):
        self.request_handler = request_handler

    def execute(self, params: GetDeviceInfoQueryParams | None = None) -> HttpResponse[DeviceInfoReadModel]:
        if params is None:
            return HttpResponse.fail(message="You need to specify an ip")
        return HttpResponse.ok(self.request_handler.retrieve_device_info())
