from abc import ABC, abstractmethod

from apps.communication.communication_responses.communication_response import CommunicationResponse

from data_backend.communication_system.domain.communication_system_client import CommunicationSystemClient


class CommunicationRequestHandler(ABC):
    def __init__(self, drifter_client: CommunicationSystemClient):
        self.drifter_client = drifter_client

    @abstractmethod
    def ping_drifter(self) -> CommunicationResponse:
        pass

    @abstractmethod
    def ping_localizer(self) -> CommunicationResponse:
        pass
