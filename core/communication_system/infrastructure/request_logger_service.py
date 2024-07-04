from core.communication_system.application.ports.communication_request_history_repository import CommunicationRequestHistoryRepository
from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.shared.domain.http.httpexception import PreviousUnresolvedRequestException


class CommunicationRequestLoggerService:
    def __init__(self, repository: CommunicationRequestHistoryRepository):
        self.request_logger_repository = repository

    def log_request(self, request: CommunicationRequest) -> None:
        available_req = self.request_logger_repository.get_latest_unresolved_communication_request_for_op_code(request.op_code)
        if available_req:
            raise PreviousUnresolvedRequestException("There is already an unresolved request for this operation")
        self.request_logger_repository.add_communication_request(request)

    def resolve_request(self, op_code: chr, recipient: int) -> None:
        self.request_logger_repository.resolve_communication_request(op_code, recipient)
