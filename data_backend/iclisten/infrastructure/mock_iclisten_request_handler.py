from data_backend.iclisten.domain import ICListenClient
from data_backend.iclisten.application.ports.iclisten_request_handler import ICListenRequestHandler
from data_backend.iclisten.domain.device_info_read_model import DeviceStatusReadModel, DeviceInfoReadModel, \
    RecordingStatusReadModel, AboutReadModel


class MockICListenRequestHandler(ICListenRequestHandler):

    def __init__(self, iclisten_client: ICListenClient):
        self.iclisten_client = iclisten_client

    def retrieve_device_info(self) -> DeviceInfoReadModel:
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

        device_info = DeviceInfoReadModel(
            device_status=device_status,
            recording_status=recording_status,
            about=about
        )
        return device_info

    def job_setup(self) -> None:
        pass
