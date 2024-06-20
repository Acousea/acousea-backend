from apps.communication.communication_requests.ping_drifter_request.ping_drifter_request import PingDrifterRequest
from apps.communication.communication_requests.ping_localizer_request.ping_localizer_request import PingLocalizerRequest
from apps.communication.communication_responses.communication_response import CommunicationResponse
from data_backend.communication_system.domain.communication_system_client import CommunicationSystemClient


class SerialCommunicationSystemRequestHandler:
    def __init__(self, communication_system_client: CommunicationSystemClient):
        self.client = communication_system_client

    def ping_drifter(self) -> CommunicationResponse:
        response = self.client.ping_drifter()
        # Check if the response content is the same as the request content
        if response.content() == PingDrifterRequest.content:
            return response
        else:
            raise ValueError("Ping failed")

    def ping_localizer(self) -> CommunicationResponse:
        response = self.client.ping_localizer()
        # Check if the response content is the same as the request content
        if response.content() == PingLocalizerRequest.content:
            return response
        else:
            raise ValueError("Ping failed")
