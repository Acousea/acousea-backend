from abc import ABC, abstractmethod

from core.communication_system.domain.communicator.communication_request import CommunicationRequest


class CommunicationRequestHistoryRepository(ABC):
    @abstractmethod
    def add_communication_request(self, request: CommunicationRequest) -> None:
        pass

    @abstractmethod
    def get_latest_resolved_communication_request_for_op_code(self, op_code: int) -> CommunicationRequest | None:
        pass

    @abstractmethod
    def get_latest_unresolved_communication_request_for_op_code(self, op_code: int) -> CommunicationRequest | None:
        pass

    @abstractmethod
    def get_latest_resolved_communication_request(self) -> CommunicationRequest | None:
        pass

    @abstractmethod
    def get_latest_unresolved_communication_request(self) -> CommunicationRequest | None:
        pass

    @abstractmethod
    def get_all_communication_requests(self) -> list[CommunicationRequest] | None:
        pass

    @abstractmethod
    def flush_all_unresolved_requests(self):
        pass

    @abstractmethod
    def resolve_communication_request(self, op_code: chr, recipient: int):
        pass
