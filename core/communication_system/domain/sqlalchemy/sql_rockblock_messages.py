# database.py
import datetime

from sqlalchemy import UUID, Column, Integer, String, Float, DateTime

from core.communication_system.domain.rockblock_message import RockBlockMessage
from core.shared.domain.db import Base, engine
from core.shared.domain.value_objects import GenericUUID


class SQLRockBlockMessage(Base):
    __tablename__ = "rockblock_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    imei = Column(String, index=True)
    serial = Column(String)
    momsn = Column(Integer)
    transmit_time = Column(DateTime, default=datetime.datetime.utcnow)
    iridium_latitude = Column(Float)
    iridium_longitude = Column(Float)
    iridium_cep = Column(Integer)
    data = Column(String)

    @staticmethod
    def from_rockblock_message(packet: RockBlockMessage) -> "SQLRockBlockMessage":
        return SQLRockBlockMessage(
            id=GenericUUID.next_id(),
            imei=packet.imei,
            serial=packet.serial,
            momsn=packet.momsn,
            transmit_time=datetime.datetime.strptime(packet.transmit_time, '%y-%m-%d %H:%M:%S'),
            iridium_latitude=packet.iridium_latitude,
            iridium_longitude=packet.iridium_longitude,
            iridium_cep=packet.iridium_cep,
            data=packet.data
        )

    def to_rockblock_message(self) -> RockBlockMessage:
        return RockBlockMessage(
            imei=self.imei,
            serial=self.serial,
            momsn=self.momsn,
            transmit_time=self.transmit_time.strftime('%y-%m-%d %H:%M:%S'),
            iridium_latitude=self.iridium_latitude,
            iridium_longitude=self.iridium_longitude,
            iridium_cep=self.iridium_cep,
            data=self.data
        )


Base.metadata.create_all(bind=engine)
