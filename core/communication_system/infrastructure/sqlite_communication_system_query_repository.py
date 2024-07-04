from typing import Type

from sqlalchemy.orm import Session

from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.communication_system.domain.communicator.responses.drifter_simple_report_response import DrifterSimpleReportResponse
from core.communication_system.domain.communicator.responses.localizer_simple_report_response import \
    LocalizerSimpleReportResponse
from core.communication_system.domain.sqlalchemy.sql_drifter_device_info import SQLDrifterDeviceInfo
from core.communication_system.domain.sqlalchemy.sql_localizer_device_info import SQLLocalizerDeviceInfo


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
        if drifter_info:
            drifter_info.operation_mode = op_mode
            self.db.add(drifter_info)
            self.db.commit()

    def store_localizer_op_mode(self, op_mode: int):
        # copy the last registered localizer info and update the operation mode
        localizer_info: Type[SQLLocalizerDeviceInfo] = self.db.query(SQLLocalizerDeviceInfo).order_by(SQLLocalizerDeviceInfo.timestamp.desc()).first()
        if localizer_info:
            localizer_info.operation_mode = op_mode
            self.db.add(localizer_info)
            self.db.commit()
