from data_backend.device.info.application.ports.device_info_query_repository import DeviceInfoQueryRepository
from data_backend.device.info.domain.device_info_read_model import (
    DeviceInfoReadModel,
    DeviceStatusReadModel,
    RecordingStatusReadModel,
    EventStatusReadModel,
    AboutReadModel
)


class MockDeviceInfoQueryRepository(DeviceInfoQueryRepository):

    def get_all(self) -> DeviceInfoReadModel:
        device_status = DeviceStatusReadModel(
            unitStatus="MOCKED",
            battery="99% (Not Charging)",
            unitTime="Fri, 01 Jan 2010 23:44:55 UTC",
            timeSync="No PPS",
            temperature="29.6°C",
            humidity="31.7%"
        )

        recording_status = RecordingStatusReadModel(
            recordWAV="Off (50 kHz)",
            recordFFT="Off (200 kHz)"
        )

        event_status = EventStatusReadModel(
            noSignalEventInactive="No Signal, Event Inactive",
            signalPresentEventInactive="Signal Present, Event Inactive",
            signalPresentEventActive="Signal Present, Event Active",
            noSignalEventActive="No Signal, Event Active"
        )

        about = AboutReadModel(
            firmwareRelease="40.0",
            hardwareRelease="4",
            ipAddress="192.168.10.150",
            macAddress="00:08:EE:40:80:28",
            hydrophoneSensitivity="-177.2 dBV re µPa",
            memoryCapacity="128 GB"
        )

        device_info = DeviceInfoReadModel(
            deviceStatus=device_status,
            recordingStatus=recording_status,
            eventStatus=event_status,
            epochs=[1, 2, 3, 4, 5],
            tilt="",
            about=about
        )

        return device_info
