from apps.communication.communication_responses.get_device_info_response.get_device_info_response import \
    GetDeviceInfoResponse
from data_backend.iclisten.domain import ICListenClient
from data_backend.iclisten.application.ports.iclisten_request_handler import ICListenRequestHandler
from data_backend.iclisten.domain.device_info_read_model import DeviceStatusReadModel, DeviceInfoReadModel, \
    RecordingStatusReadModel, AboutReadModel


class SerialICListenRequestHandler(ICListenRequestHandler):

    def __init__(self, iclisten_client: ICListenClient):
        super().__init__(iclisten_client)

    def retrieve_device_info(self) -> DeviceInfoReadModel:
        device_status: GetDeviceInfoResponse = self.iclisten_client.get_device_info()

        return DeviceInfoReadModel(
            device_status=DeviceStatusReadModel(
                unit_status=str(device_status.unit_status),
                battery_status=str(device_status.battery_status),
                unit_time=str(device_status.unit_time),
                time_sync=str(device_status.time_sync),
                temperature=str(device_status.temperature),
                humidity=str(device_status.humidity),
                hydrophone_sensitivity=str(device_status.hydrophone_sensitivity)
            ),
            recording_status=RecordingStatusReadModel(
                record_wav=str(device_status.record_wav),
                wav_sample_rate=str(device_status.waveform_sample_rate),
                record_fft=str(device_status.record_fft),
                fft_sample_rate=str(device_status.fft_sample_rate)
            ),
            about=AboutReadModel(
                firmware_release=str(device_status.firmware_release),
                hardware_release=str(device_status.hardware_release),
                ip_address=str(device_status.ip_address)
            )
        )

    def job_setup(self) -> None:
        pass
