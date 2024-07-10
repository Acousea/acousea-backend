# database.py
import datetime
from sqlalchemy import Column, Integer, Float, DateTime, UUID
from core.communication_system.domain.communicator.responses.drifter_simple_report_response import DrifterSimpleReportResponse
from core.communication_system.domain.read_models.communication_system_status_read_model import CommunicationSystemStatusReadModel

from core.shared.domain.db_dependencies import Base
from core.shared.domain.read_models.storage_read_model import StorageReadModel
from core.shared.domain.value_objects import GenericUUID


class SQLDrifterDeviceInfo(Base):
    __tablename__ = "drifter_device_info"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    epoch_time = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    battery_percent = Column(Integer)
    battery_status = Column(Integer)
    temperature = Column(Float)
    operation_mode = Column(Integer)
    storage_total = Column(Integer)
    storage_free = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def from_get_device_info_response(response: DrifterSimpleReportResponse) -> "SQLDrifterDeviceInfo":
        return SQLDrifterDeviceInfo(
            id=GenericUUID.next_id(),
            epoch_time=datetime.datetime.utcfromtimestamp(response.epoch_time),
            battery_percentage=response.battery_percentage,
            battery_status=response.battery_status,
            latitude=response.latitude,
            longitude=response.longitude,
            temperature=response.temperature,
            operation_mode=response.operation_mode,
            storage_total=response.storage_total,
            storage_free=response.storage_free,
            timestamp=datetime.datetime.utcnow()
        )

    def to_device_info_read_model(self) -> CommunicationSystemStatusReadModel:
        return CommunicationSystemStatusReadModel(
            epoch_time=str(datetime.datetime.strftime(self.epoch_time, "%Y-%m-%d %H:%M:%S")),
            battery_percentage=self.battery_percent,
            battery_status=self.battery_status,
            latitude=self.latitude,
            longitude=self.longitude,
            operation_mode=self.operation_mode,
            temperature=self.temperature,
            storage=StorageReadModel(
                total=self.storage_total,
                free=self.storage_free
            )
        )
