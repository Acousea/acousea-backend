# database.py
import datetime

from sqlalchemy import Column, Integer, Float, DateTime, UUID

from core.communication_system.domain.communicator.responses.drifter_summary_report_response import DrifterSummaryReportResponse
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
    battery_percentage = Column(Integer)
    battery_status = Column(Integer)
    temperature = Column(Float)
    operation_mode = Column(Integer)
    storage_total = Column(Integer)
    storage_used = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def from_get_device_info_response(response: DrifterSummaryReportResponse) -> "SQLDrifterDeviceInfo":
        return SQLDrifterDeviceInfo(
            id=GenericUUID.next_id(),
            epoch_time=datetime.datetime.utcfromtimestamp(response.epoch_time),
            operation_mode=response.drifter_module_operation_mode,
            battery_percentage=response.drifter_module_battery_percentage,
            battery_status=response.drifter_module_battery_status,
            latitude=response.latitude,
            longitude=response.longitude,
            temperature=response.drifter_module_temperature,
            storage_total=response.drifter_module_storage_total,
            storage_used=response.drifter_module_storage_used,
            timestamp=datetime.datetime.utcnow()
        )

    def to_device_info_read_model(self) -> CommunicationSystemStatusReadModel:
        return CommunicationSystemStatusReadModel(
            timestamp=str(datetime.datetime.strftime(self.timestamp, "%Y-%m-%d %H:%M:%S")),
            epoch_time=str(datetime.datetime.strftime(self.epoch_time, "%Y-%m-%d %H:%M:%S")),
            battery_percentage=self.battery_percentage, 
            battery_status=self.battery_status,
            latitude=self.latitude,
            longitude=self.longitude,
            operation_mode=self.operation_mode,
            temperature=self.temperature,
            storage=StorageReadModel(
                total=self.storage_total,
                used=self.storage_used
            )
        )
