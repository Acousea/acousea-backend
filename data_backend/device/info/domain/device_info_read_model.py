from pydantic import BaseModel
from typing import List


class DeviceStatusReadModel(BaseModel):
    unitStatus: str
    battery: str
    unitTime: str
    timeSync: str
    temperature: str
    humidity: str


class RecordingStatusReadModel(BaseModel):
    recordWAV: str
    recordFFT: str


class EventStatusReadModel(BaseModel):
    noSignalEventInactive: str
    signalPresentEventInactive: str
    signalPresentEventActive: str
    noSignalEventActive: str


class AboutReadModel(BaseModel):
    firmwareRelease: str
    hardwareRelease: str
    ipAddress: str
    macAddress: str
    hydrophoneSensitivity: str
    memoryCapacity: str


class DeviceInfoReadModel(BaseModel):
    deviceStatus: DeviceStatusReadModel
    recordingStatus: RecordingStatusReadModel
    eventStatus: EventStatusReadModel
    epochs: List[int]
    tilt: str
    about: AboutReadModel
