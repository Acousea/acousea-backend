# database.py
import datetime

from sqlalchemy import Column, Integer, Float, DateTime, UUID

from core.communication_system.domain.communicator.responses.drifter_simple_report_response import DrifterSimpleReportResponse
from core.communication_system.domain.read_models.drifter_device_info_read_model import DrifterDeviceInfoReadModel
from core.shared.domain.db_dependencies import Base, engine
from core.shared.domain.value_objects import GenericUUID


class SQLDrifterDeviceInfo(Base):
    __tablename__ = "drifter_device_info"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    epoch_time = Column(DateTime)
    battery_percent = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    operation_mode = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def from_get_device_info_response(response: DrifterSimpleReportResponse) -> "SQLDrifterDeviceInfo":
        return SQLDrifterDeviceInfo(
            id=GenericUUID.next_id(),
            epoch_time=datetime.datetime.utcfromtimestamp(response.epoch_time),
            battery_percent=response.battery_percent,
            latitude=response.latitude,
            longitude=response.longitude,
            operation_mode=response.operation_mode,
            timestamp=datetime.datetime.utcnow()
        )

    def to_device_info_read_model(self) -> DrifterDeviceInfoReadModel:

        return DrifterDeviceInfoReadModel(
            epoch_time=str(datetime.datetime.strftime(self.epoch_time, "%Y-%m-%d %H:%M:%S")),
            battery_percent=self.battery_percent,
            latitude=self.latitude,
            longitude=self.longitude,
            operation_mode=self.operation_mode,
        )


# Base.metadata.create_all(bind=engine)  # This is done in the DBManager
