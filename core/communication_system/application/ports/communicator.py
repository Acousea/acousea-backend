from abc import ABC, abstractmethod

from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.communication_system.domain.communicator.communication_result import CommunicationResult


class Communicator(ABC):
    @abstractmethod
    def send_request(self, request: CommunicationRequest) -> CommunicationResult:
        pass

    @abstractmethod
    def close(self):
        pass
