from core.iclisten.application.ports.iclisten_repository import PAMSystemRepository
from core.iclisten.domain.pam_system_logging_config_read_model import PAMDeviceLoggingConfigReadModel

from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetDeviceLoggingConfigHttpRequest(HttpRequest[None, PAMDeviceLoggingConfigReadModel]):
    def __init__(self, pam_system_repository: PAMSystemRepository):
        self.pam_system_repository = pam_system_repository

    def execute(self, params: None = None) -> HttpResponse[PAMDeviceLoggingConfigReadModel]:
        pam_device_status_info: PAMDeviceLoggingConfigReadModel = self.pam_system_repository.get_pam_device_logging_config()
        return HttpResponse.ok(
            pam_device_status_info
        )
