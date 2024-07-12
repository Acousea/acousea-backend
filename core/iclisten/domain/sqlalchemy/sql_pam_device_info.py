# database.py
import datetime

from sqlalchemy import Column, Integer, Float, DateTime, UUID

from core.communication_system.domain.communicator.responses.drifter_summary_report_response import DrifterSummaryReportResponse
from core.iclisten.domain.communicator.get_pam_device_info_response import GetPAMDeviceInfoCommunicationResponse
from core.iclisten.domain.pam_system_status_info_read_model import PAMDeviceStatusReadModel
from core.shared.domain.db_dependencies import Base
from core.shared.domain.value_objects import GenericUUID


class SQLPAMDeviceInfo(Base):
    __tablename__ = "pam_device_status_info"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    unit_status = Column(Integer)
    battery_status = Column(Integer)
    battery_percentage = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def from_get_device_info_response(response: GetPAMDeviceInfoCommunicationResponse) -> "SQLPAMDeviceInfo":
        return SQLPAMDeviceInfo(
            id=GenericUUID.next_id(),
            unit_status=response.unit_status,
            battery_status=response.battery_status,
            battery_percentage=response.battery_percentage,
            temperature=response.temperature,
            humidity=response.humidity
        )

    @staticmethod
    def from_drifter_summary_report_response(response: DrifterSummaryReportResponse) -> "SQLPAMDeviceInfo":
        return SQLPAMDeviceInfo(
            id=GenericUUID.next_id(),
            unit_status=response.pam_device_unit_status,
            battery_status=response.pam_device_battery_status,
            battery_percentage=response.pam_device_battery_percentage,
            temperature=response.pam_device_temperature,
            humidity=response.pam_device_humidity
        )

    def to_device_info_read_model(self) -> PAMDeviceStatusReadModel:
        return PAMDeviceStatusReadModel(
            unit_status=self.unit_status,
            battery_status=self.battery_status,
            battery_percentage=self.battery_percentage,
            temperature=self.temperature,
            humidity=self.humidity
        )

    @staticmethod
    def get_unit_status_description(status: int) -> str:
        status_map = {
            0: "Ready",
            1: "Data Acquisition Not Ready",
            2: "Device Not Ready",
            3: "Start-up Configuration Failed",
            4: "Baud Rate Reconfiguring",
            5: "File System Fault",
            6: "Off"
        }
        return status_map.get(status, "Unknown")

    @staticmethod
    def get_date_from_unix_timestamp(timestamp: int) -> str:
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_system_time_status(status: int) -> str:
        status_str = ''
        if 128 <= status <= 137:
            status = str(status - 128)
            status_str += "Time set from PPS encoded time. "

        status_map = {
            0: "Time value has not been set",
            1: "Time was manually set",
            2: "Time set from RTC at start-up",
            3: "Time was set from file system at start-up",
            4: "Time was set from NTP",
            5: "Time was set from GPS",
            6: "Time was set from PTP",
        }

        status_str += status_map.get(status, "Unknown")
        return status_str

# Base.metadata.create_all(bind=engine) # This is done in the DBManager
