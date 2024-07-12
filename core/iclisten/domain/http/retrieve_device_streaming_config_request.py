from core.iclisten.application.ports.iclisten_repository import PAMSystemRepository
from core.iclisten.domain.pam_system_streaming_config_read_model import PAMDeviceStreamingConfigReadModel

from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class RetrieveDeviceStreamingConfigHttpRequest(HttpRequest[None, PAMDeviceStreamingConfigReadModel]):
    def __init__(self, pam_system_repository: PAMSystemRepository):
        self.pam_system_repository = pam_system_repository

    def execute(self, params: None = None) -> HttpResponse[PAMDeviceStreamingConfigReadModel]:
        pam_device_status_info: PAMDeviceStreamingConfigReadModel = self.pam_system_repository.get_streaming_config()
        return HttpResponse.ok(
            pam_device_status_info
        )
