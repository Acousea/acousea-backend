from core.iclisten.application.ports.iclisten_repository import ICListenRepository
from core.iclisten.domain.communicator.get_device_info_response import GetDeviceInfoResponse
from core.iclisten.domain.iclisten_device_info_read_model import ICListenDeviceInfoReadModel, DeviceStatusReadModel, RecordingStatusReadModel, AboutReadModel
from core.iclisten.domain.job_setup_read_model import JobSetupReadModel
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel


class MockICListenRepository(ICListenRepository):
    def get_device_info(self) -> ICListenDeviceInfoReadModel:
        device_status = DeviceStatusReadModel(
            unit_status="MOCKED",
            battery_status="99% (Not Charging)",
            unit_time="Fri, 01 Jan 2010 23:44:55 UTC",
            time_sync="No PPS",
            temperature="29.6°C",
            humidity="31.7%",
            hydrophone_sensitivity="-177.2 dBV re µPa"
        )

        recording_status = RecordingStatusReadModel(
            record_wav="Off (50 kHz)",
            record_fft="Off (200 kHz)"
        )

        about = AboutReadModel(
            firmware_release="40.0",
            hardware_release="4",
            ip_address="192.168.10.150",
            mac_address="00:08:EE:40:80:28",
        )

        device_info = ICListenDeviceInfoReadModel(
            device_status=device_status,
            recording_status=recording_status,
            about=about
        )
        return device_info

    def get_job_setup(self) -> JobSetupReadModel:
        pass

    def get_latest_stats(self, limit: int = 5) -> RecordingStatsReadModel:
        pass

    def add_device_info(self, device_info: GetDeviceInfoResponse) -> None:
        pass


