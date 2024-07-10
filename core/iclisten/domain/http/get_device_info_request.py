from core.iclisten.application.ports.iclisten_repository import PAMSystemRepository
from core.iclisten.domain.pam_system_status_info_read_model import PAMDeviceStatusReadModel
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetDeviceInfoHttpRequest(HttpRequest[None, PAMDeviceStatusReadModel]):
    def __init__(self, pam_system_repository: PAMSystemRepository):
        self.pam_system_repository = pam_system_repository

    def execute(self, params: None = None) -> HttpResponse[PAMDeviceStatusReadModel]:
        pam_device_status_info: PAMDeviceStatusReadModel = self.pam_system_repository.get_pam_device_status_info()
        return HttpResponse.ok(
            pam_device_status_info
        )
