from apps.communication.communication_responses.communication_response import CommunicationResponse
from data_backend.drifter.application.ports.drifter_request_handler import DrifterRequestHandler
from data_backend.drifter.domain.drifter_client import DrifterClient


class SerialDrifterRequestHandler(DrifterRequestHandler):
    def __init__(self, drifter_client: DrifterClient):
        super().__init__(drifter_client)

    def ping(self) -> CommunicationResponse:
        response = self.drifter_client.ping()
        # Check if the response content is the same as the request content
        if response.content() == b'\x00\xFF\x00\xFF':
            return response
        else:
            raise ValueError("Ping failed")

