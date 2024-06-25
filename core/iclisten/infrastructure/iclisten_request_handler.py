from core.iclisten.domain.communicator.get_device_info_request import GetDeviceInfoRequest
from core.iclisten.domain.communicator.get_device_info_response import GetDeviceInfoResponse
from core.iclisten.domain.device_info_read_model import DeviceStatusReadModel, DeviceInfoReadModel, \
    RecordingStatusReadModel, AboutReadModel
from core.shared.application.communicator import Communicator


class ICListenRequestHandler:

    def __init__(self, communicator: Communicator):
        self.communicator = communicator

    def retrieve_device_info(self) -> DeviceInfoReadModel:
        response_packet = self.communicator.send_request(GetDeviceInfoRequest())
        device_status: GetDeviceInfoResponse = GetDeviceInfoResponse(response_packet)  # Convertimos la respuesta genérica a específica

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
