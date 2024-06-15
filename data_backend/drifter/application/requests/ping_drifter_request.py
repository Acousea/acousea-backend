from pydantic import BaseModel

from apps.communication.communication_requests.mock_communication_request.mock_communication_request import \
    MockCommunicationRequest
from apps.communication.iclisten_client.ICListenClient import ICListenClient
from apps.communication.iclisten_client.communicator.communicator import Communicator
from data_backend.shared.application.httprequest import HttpRequest
from data_backend.shared.domain.httpresponse import HttpResponse


class PingDrifterResponse(BaseModel):
    message: str


class PingDrifterRequest(HttpRequest[None, PingDrifterResponse]):
    def __init__(self, communicator: Communicator):
        self.communicator = communicator

    def execute(self, params: None = None) -> HttpResponse[PingDrifterResponse]:
        ic_listen_client = ICListenClient(self.communicator)
        ping_request = MockCommunicationRequest()
        response = ic_listen_client.send(ping_request)
        if response.empty():
            return HttpResponse.fail(message="No response")
        if response.response[3:-1] != ping_request.payload:
            return HttpResponse.fail(message="Bad response")
        return HttpResponse.ok(PingDrifterResponse(message="Drifter is alive"))
