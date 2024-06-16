from abc import ABC, abstractmethod
from typing import Type

from apps.communication.communication_requests.communication_request import CommunicationRequest
from apps.communication.communication_responses.communication_response import CommunicationResponse


class Communicator(ABC):
    @abstractmethod
    def send_request(self, request: CommunicationRequest, response_cls: Type[CommunicationResponse]) -> CommunicationResponse:
        pass

    @abstractmethod
    def close(self):
        pass
