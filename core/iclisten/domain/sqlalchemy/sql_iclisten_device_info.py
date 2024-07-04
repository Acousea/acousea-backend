# database.py
import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, UUID

from core.iclisten.domain.communicator.get_device_info_response import GetDeviceInfoResponse
from core.iclisten.domain.iclisten_device_info_read_model import ICListenDeviceInfoReadModel, DeviceStatusReadModel, RecordingStatusReadModel, \
    AboutReadModel
from core.shared.domain.db_dependencies import Base
from core.shared.domain.value_objects import GenericUUID


class SQLICListenDeviceInfo(Base):
    __tablename__ = "iclisten_device_info"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    unit_status = Column(Integer)
    battery_status = Column(Integer)
    unit_time = Column(Integer)
    system_time_status = Column(Integer)
    temperature = Column(Float)
    humidity = Column(Float)
    hydrophone_sensitivity = Column(Float)
    record_wav = Column(Integer)
    waveform_sample_rate = Column(Integer)
    record_fft = Column(Integer)
    fft_sample_rate = Column(Integer)
    firmware_release = Column(String)
    hardware_release = Column(String)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def from_get_device_info_response(response: GetDeviceInfoResponse) -> "SQLICListenDeviceInfo":
        return SQLICListenDeviceInfo(
            id=GenericUUID.next_id(),
            unit_status=response.unit_status,
            battery_status=response.battery_status,
            unit_time=response.unit_time,
            time_sync=response.time_sync,
            temperature=response.temperature,
            humidity=response.humidity,
            hydrophone_sensitivity=response.hydrophone_sensitivity,
            record_wav=response.record_wav,
            waveform_sample_rate=response.waveform_sample_rate,
            record_fft=response.record_fft,
            fft_sample_rate=response.fft_sample_rate,
            firmware_release=response.firmware_release,
            hardware_release=response.hardware_release,
            ip_address=response.ip_address
        )

    def to_device_info_read_model(self) -> ICListenDeviceInfoReadModel:
        return ICListenDeviceInfoReadModel(
            device_status=DeviceStatusReadModel(
                unit_status=self.get_unit_status_description(self.unit_status),
                battery_status=str(self.battery_status) + "%",
                unit_time=self.get_date_from_unix_timestamp(self.unit_time),
                system_time_status=self.get_system_time_status(self.system_time_status),
                temperature=str(round(self.temperature, 2)),
                humidity=str(round(self.humidity, 2)),
                hydrophone_sensitivity=str(round(self.hydrophone_sensitivity, 2)),
            ),
            recording_status=RecordingStatusReadModel(
                record_wav=str(self.record_wav),
                wav_sample_rate=str(self.waveform_sample_rate),
                record_fft=str(self.record_fft),
                fft_sample_rate=str(self.fft_sample_rate),
            ),
            about=AboutReadModel(
                firmware_release=self.firmware_release,
                hardware_release=self.hardware_release,
                ip_address=self.ip_address,
            )
        )

    @staticmethod
    def get_unit_status_description(status: int) -> str:
        if status == 0:
            return "Ready"
        elif status == 1:
            return "Data Acquisition Not Ready"
        elif status == 2:
            return "Device Not Ready"
        elif status == 3:
            return "Start-up Configuration Failed"
        elif status == 4:
            return "Baud Rate Reconfiguring"
        elif status == 5:
            return "File System Fault"
        else:
            return "Unknown"

    @staticmethod
    def get_date_from_unix_timestamp(timestamp: int) -> str:
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_system_time_status(status: int) -> str:
        status_str = ''
        if 128 <= status <= 137:
            status = str(status - 128)
            status_str += "Time set from PPS encoded time. "

        if status == 0:
            status_str += "Time value has not been set"
        elif status == 1:
            status_str += "Time was manually set"
        elif status == 2:
            status_str += "Time set from RTC at start-up"
        elif status == 3:
            status_str += "Time was set from file system at start-up"
        elif status == 4:
            status_str += "Time was set from NTP"
        elif status == 5:
            status_str += "Time was set from GPS"
        elif status == 6:
            status_str += "Time was set from PTP"
        else:
            status_str += "Unknown"

        return status_str

# Base.metadata.create_all(bind=engine) # This is done in the DBManager
