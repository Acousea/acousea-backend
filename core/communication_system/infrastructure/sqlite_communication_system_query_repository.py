import datetime
from typing import Type

from sqlalchemy.orm import Session

from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.communication_system.domain.communicator.responses.drifter_simple_report_response import DrifterSimpleReportResponse
from core.communication_system.domain.communicator.responses.localizer_simple_report_response import LocalizerSimpleReportResponse
from core.communication_system.domain.read_models.communication_system_status_read_model import CommunicationSystemStatusReadModel
from core.communication_system.domain.sqlalchemy.sql_drifter_device_info import SQLDrifterDeviceInfo
from core.communication_system.domain.sqlalchemy.sql_localizer_device_info import SQLLocalizerDeviceInfo
from core.shared.domain.value_objects import GenericUUID


class SQLiteCommunicationSystemQueryRepository(CommunicationSystemQueryRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_drifter_op_mode(self) -> int | None:
        drifter_info: Type[SQLDrifterDeviceInfo] = self.db.query(SQLDrifterDeviceInfo).order_by(SQLDrifterDeviceInfo.timestamp.desc()).first()
        if drifter_info:
            return drifter_info.to_device_info_read_model().operation_mode
        return None

    def get_localizer_op_mode(self) -> int | None:
        localizer_info: Type[SQLLocalizerDeviceInfo] = self.db.query(SQLLocalizerDeviceInfo).order_by(SQLLocalizerDeviceInfo.timestamp.desc()).first()
        if localizer_info:
            return localizer_info.to_device_info_read_model().operation_mode
        return None

    def get_drifter_location(self) -> tuple[float, float] | None:
        drifter_location = self.db.query(SQLDrifterDeviceInfo).order_by(SQLDrifterDeviceInfo.timestamp.desc()).first()
        if drifter_location:
            drifter_device_info = drifter_location.to_device_info_read_model()
            return drifter_device_info.latitude, drifter_device_info.longitude
        return None

    def get_localizer_location(self) -> tuple[float, float] | None:
        localizer_location = self.db.query(SQLLocalizerDeviceInfo).order_by(SQLLocalizerDeviceInfo.timestamp.desc()).first()
        if localizer_location:
            localizer_device_info = localizer_location.to_device_info_read_model()
            return localizer_device_info.latitude, localizer_device_info.longitude
        return None

    def store_simple_report_drifter_device_info(self, drifter_info: DrifterSimpleReportResponse):
        drifter_info = SQLDrifterDeviceInfo.from_get_device_info_response(drifter_info)
        self.db.add(drifter_info)
        self.db.commit()

    def store_simple_report_localizer_device_info(self, localizer_info: LocalizerSimpleReportResponse):
        localizer_info = SQLLocalizerDeviceInfo.from_get_device_info_response(localizer_info)
        self.db.add(localizer_info)
        self.db.commit()

    def store_drifter_op_mode(self, op_mode: int):
        # copy the last registered drifter info and update the operation mode
        drifter_info: Type[SQLDrifterDeviceInfo] = self.db.query(SQLDrifterDeviceInfo).order_by(SQLDrifterDeviceInfo.timestamp.desc()).first()
        # Copy the values of drifter info into a new object and update the operation mode
        if drifter_info:
            new_drifter_info = SQLDrifterDeviceInfo(
                id=GenericUUID.next_id(),
                epoch_time=drifter_info.epoch_time,
                battery_percentage=drifter_info.battery_percent,
                battery_status=drifter_info.battery_status,
                latitude=drifter_info.latitude,
                longitude=drifter_info.longitude,
                temperature=drifter_info.temperature,
                operation_mode=op_mode,
                storage_total=drifter_info.storage_total,
                storage_free=drifter_info.storage_free,
                timestamp=datetime.datetime.utcnow()
            )
            self.db.add(new_drifter_info)
            self.db.commit()

    def store_localizer_op_mode(self, op_mode: int):
        # copy the last registered localizer info and update the operation mode
        localizer_info: Type[SQLLocalizerDeviceInfo] = self.db.query(SQLLocalizerDeviceInfo).order_by(SQLLocalizerDeviceInfo.timestamp.desc()).first()
        if localizer_info:
            new_localizer_info = SQLLocalizerDeviceInfo(
                id=GenericUUID.next_id(),
                epoch_time=localizer_info.epoch_time,
                battery_percentage=localizer_info.battery_percent,
                battery_status=localizer_info.battery_status,
                latitude=localizer_info.latitude,
                longitude=localizer_info.longitude,
                temperature=localizer_info.temperature,
                operation_mode=op_mode,
                storage_total=localizer_info.storage_total,
                storage_free=localizer_info.storage_free,
                timestamp=datetime.datetime.utcnow()
            )
            self.db.add(new_localizer_info)
            self.db.commit()

    def get_communication_system_status(self) -> CommunicationSystemStatusReadModel:
        # Query the database for the latest communication system status and convert it to the domain read model format
        communication_status: Type[SQLDrifterDeviceInfo] = (
            self.db.query(SQLDrifterDeviceInfo)
            .order_by(SQLDrifterDeviceInfo.timestamp.desc())
            .first()
        )

        if communication_status is None:
            raise Exception("No recent drifter device status found")

        return communication_status.to_device_info_read_model()
