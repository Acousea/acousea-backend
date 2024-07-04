from typing import Type

from sqlalchemy.orm import Session

from core.communication_system.application.ports.communication_request_history_repository import CommunicationRequestHistoryRepository
from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.communication_system.domain.sqlalchemy.sql_communication_request_history import SQLCommunicationRequestHistory


class SQLCommunicationRequestHistoryRepository(CommunicationRequestHistoryRepository):

    def __init__(self, db=Session):
        self.db = db

    def add_communication_request(self, request: CommunicationRequest) -> None:
        sql_comm_req = SQLCommunicationRequestHistory.from_communication_request(request)
        self.db.add(sql_comm_req)
        self.db.commit()

    def get_latest_resolved_communication_request_for_op_code(self, op_code: int) -> CommunicationRequest | None:
        sql_comm_req: Type[SQLCommunicationRequestHistory] = (
            self.db.query(SQLCommunicationRequestHistory)
            .filter(SQLCommunicationRequestHistory.op_code == op_code)
            .filter(SQLCommunicationRequestHistory.is_resolved == True)
            .order_by(SQLCommunicationRequestHistory.timestamp.desc())
            .first()
        )
        if sql_comm_req is not None:
            return sql_comm_req.to_communication_request()
        return None

    def get_latest_unresolved_communication_request_for_op_code(self, op_code: int) -> CommunicationRequest | None:
        sql_comm_req: Type[SQLCommunicationRequestHistory] = (
            self.db.query(SQLCommunicationRequestHistory)
            .filter(SQLCommunicationRequestHistory.op_code == op_code)
            .filter(SQLCommunicationRequestHistory.is_resolved == False)
            .order_by(SQLCommunicationRequestHistory.timestamp.desc())
            .first()
        )
        if sql_comm_req is None:
            return None
        return sql_comm_req.to_communication_request()

    def get_latest_resolved_communication_request(self) -> CommunicationRequest | None:
        sql_comm_req: Type[SQLCommunicationRequestHistory] = (
            self.db.query(SQLCommunicationRequestHistory)
            .filter(SQLCommunicationRequestHistory.is_resolved == True)
            .order_by(SQLCommunicationRequestHistory.timestamp.desc())
            .first()
        )
        if sql_comm_req is not None:
            return sql_comm_req.to_communication_request()
        return None

    def get_latest_unresolved_communication_request(self) -> CommunicationRequest | None:
        sql_comm_req: Type[SQLCommunicationRequestHistory] = (
            self.db.query(SQLCommunicationRequestHistory)
            .filter(SQLCommunicationRequestHistory.is_resolved == False)
            .order_by(SQLCommunicationRequestHistory.timestamp.desc())
            .first()
        )
        if sql_comm_req is not None:
            return sql_comm_req.to_communication_request()
        return None

    def get_all_communication_requests(self) -> list[CommunicationRequest] | None:
        sql_comm_reqs: list[Type[SQLCommunicationRequestHistory]] = (
            self.db.query(SQLCommunicationRequestHistory)
            .all()
        )
        if sql_comm_reqs is not None:
            return [comm_req.to_communication_request() for comm_req in sql_comm_reqs]
        return None

    def flush_all_unresolved_requests(self):
        self.db.query(SQLCommunicationRequestHistory).filter(SQLCommunicationRequestHistory.is_resolved == False).delete()
        self.db.commit()

    def resolve_communication_request(self, op_code: chr, recipient_address: int):
        sql_comm_req: Type[SQLCommunicationRequestHistory] = (
            self.db.query(SQLCommunicationRequestHistory)
            .filter(SQLCommunicationRequestHistory.op_code == op_code)
            .filter(SQLCommunicationRequestHistory.recipient_address == recipient_address)
            .filter(SQLCommunicationRequestHistory.is_resolved == False)
            .order_by(SQLCommunicationRequestHistory.timestamp.desc())
            .first()
        )
        if sql_comm_req is not None:
            sql_comm_req.is_resolved = True
            self.db.commit()
        return None
