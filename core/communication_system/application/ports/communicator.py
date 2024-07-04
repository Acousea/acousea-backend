from abc import ABC, abstractmethod

from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.communication_system.domain.communicator.communication_result import CommunicationResult


class Communicator(ABC):
    def __init__(self, name: str):
        self.name = name
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def send_request(self, request: CommunicationRequest) -> CommunicationResult:
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def flush_communication_request_queue(self, localizer: bool, drifter: bool) -> CommunicationResult:
        pass
