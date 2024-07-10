from core.communication_system.domain.communicator.communication_result import CommunicationResult
from core.communication_system.infrastructure.communicator.communicator_service import CommunicatorService
from core.iclisten.domain.communicator.get_pam_device_info_request import GetDeviceInfoRequest


class ICListenClient:
    """
    Interface for ICListenClient: This client is used to send the requests to set configuration or update the
    configuration information in the persistent data store (Repository), remotely requesting the new status/config
    information from the actual device, that will not be directly received from these methods, as they will only
    inform the result of request sending operation.
    """

    def __init__(self, communicator_service: CommunicatorService):
        self.communicator_service = communicator_service

    def update_device_info(self) -> CommunicationResult:
        result = self.communicator_service.send_request(GetDeviceInfoRequest())
        return result

    def update_job_setup(self) -> CommunicationResult:
        pass

    def set_job_setup(self) -> CommunicationResult:
        pass
