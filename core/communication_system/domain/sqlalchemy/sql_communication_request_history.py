# database.py
import datetime

from sqlalchemy import Column, Integer, DateTime, UUID, BLOB, Boolean

from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.communication_system.domain.mother.communication_request_mother import CommunicationRequestMother
from core.shared.domain.db_dependencies import Base
from core.shared.domain.value_objects import GenericUUID


class SQLCommunicationRequestHistory(Base):
    __tablename__ = "communication_request_history"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    sync_byte = Column(Integer)
    op_code = Column(Integer)
    sender_address = Column(Integer)
    recipient_address = Column(Integer)
    request_type = Column(Integer)
    payload_length = Column(Integer)
    payload = Column(BLOB)
    is_resolved = Column(Boolean, default=False)

    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def from_communication_request(request: CommunicationRequest) -> "SQLCommunicationRequestHistory":
        return SQLCommunicationRequestHistory(
            id=GenericUUID.next_id(),
            sync_byte=int.from_bytes(request.sync_byte, byteorder='little'),
            op_code=request.op_code,
            sender_address=request.sender_address,
            recipient_address=request.recipient_address,
            request_type=request.request_type,
            payload_length=request.payload_length,
            payload=request.payload,
        )

    def to_communication_request(self) -> CommunicationRequest:
        # sync_byte = int.from_bytes(self.sync_byte,  byteorder='little')
        # print("sync_byte: ", sync_byte)
        return CommunicationRequest.reconstruct(
            self.sync_byte.to_bytes(1, byteorder='little'),
            str(self.op_code),
            self.sender_address,
            self.recipient_address,
            self.request_type,
            self.payload_length,
            self.payload
        )


# Base.metadata.create_all(bind=engine)  # This is done in the DBManager
if __name__ == '__main__':
    # Create a fake request
    fake_request = CommunicationRequestMother.create()
    print("---------Fake Request---------")
    print(fake_request.op_code)
    print(fake_request.sender_address)
    print(fake_request.recipient_address)
    print(fake_request.request_type)
    print(fake_request.payload_length)
    print(fake_request.payload.hex())

    # Insert the fake request into the database
    sql_request = SQLCommunicationRequestHistory.from_communication_request(fake_request)
    print("---------SQL Request---------")
    print(sql_request.op_code)
    print(sql_request.sender_address)
    print(sql_request.recipient_address)
    print(sql_request.request_type)
    print(sql_request.payload_length)
    print(sql_request.payload)

    to_comm_req = sql_request.to_communication_request()
    print("---------To Device Info---------")
    print(to_comm_req.op_code)
    print(to_comm_req.sender_address)
    print(to_comm_req.recipient_address)
    print(to_comm_req.request_type)
    print(to_comm_req.payload_length)
    print(to_comm_req.payload.hex())
