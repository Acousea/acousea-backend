from pydantic import BaseModel

from core.communication_system.infrastructure.communicator.communicator_service import CommunicatorService
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class DisableDirectCommunicationHttpResponse(BaseModel):
    message: str



class DisableDirectCommunicationHttpRequest(HttpRequest[None, DisableDirectCommunicationHttpResponse]):
    def __init__(self, communicator_service: CommunicatorService):
        self.communicator_service = communicator_service

    def execute(self, params: None = None) -> HttpResponse[DisableDirectCommunicationHttpResponse]:
        print("Before deactivation -> Selected communicator: ", self.communicator_service.selected_communicator.name)
        self.communicator_service.use_iridium_communicator()
        print("After deactivation -> Selected communicator: ", self.communicator_service.selected_communicator.name)
        return HttpResponse.ok(
            DisableDirectCommunicationHttpResponse(
                message="Direct communication successfully disabled")
        )
