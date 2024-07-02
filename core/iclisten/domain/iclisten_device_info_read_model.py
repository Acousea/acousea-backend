from pydantic import BaseModel


class DeviceStatusReadModel(BaseModel):
    unit_status: str
    battery_status: str
    unit_time: str
    system_time_status: str
    temperature: str
    humidity: str
    hydrophone_sensitivity: str


class RecordingStatusReadModel(BaseModel):
    record_wav: str
    wav_sample_rate: str
    record_fft: str
    fft_sample_rate: str


class AboutReadModel(BaseModel):
    firmware_release: str
    hardware_release: str
    ip_address: str


class ICListenDeviceInfoReadModel(BaseModel):
    device_status: DeviceStatusReadModel
    recording_status: RecordingStatusReadModel
    about: AboutReadModel
