from abc import ABC, abstractmethod

from apps.communication.communication_requests.communication_request import CommunicationRequest


class Communicator(ABC):
    @abstractmethod
    def send_request(self, request: CommunicationRequest) -> bytes:
        pass

    @abstractmethod
    def close(self):
        pass
