from abc import ABC, abstractmethod

from apps.communication.communication_responses.communication_response import CommunicationResponse
from data_backend.drifter.domain.drifter_client import DrifterClient


class DrifterRequestHandler(ABC):

    def __init__(self, drifter_client: DrifterClient):
        self.drifter_client = drifter_client

    @abstractmethod
    def ping(self) -> CommunicationResponse:
        pass


