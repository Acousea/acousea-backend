
from pydantic import BaseModel

from core.communication_system.infrastructure.communicator.communicator_service import CommunicatorService
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class EnableDirectCommunicationParams(BaseModel):
    serial_number: str


class EnableDirectCommunicationHttpResponse(BaseModel):
    message: str


class EnableDirectCommunicationHttpRequest(HttpRequest[EnableDirectCommunicationParams, EnableDirectCommunicationHttpResponse]):

    def __init__(self, communicator_service: CommunicatorService):
        self.communicator_service = communicator_service

    def execute(self, params: EnableDirectCommunicationParams | None = None) -> HttpResponse[EnableDirectCommunicationHttpResponse]:
        if params is None:
            return HttpResponse.fail(message="You need to pass a usb device serial number")
        print("Before activation -> Selected communicator: ", self.communicator_service.selected_communicator.name)
        serial_communicator_was_updated: bool = self.communicator_service.use_serial_communicator(params.serial_number)
        if not serial_communicator_was_updated:
            return HttpResponse.fail(message="No device found with the given serial number")
        print("After activation -> Selected communicator: ", self.communicator_service.selected_communicator.name)
        return HttpResponse.ok(
            EnableDirectCommunicationHttpResponse(
                message="Direct communication setup successful")
        )


