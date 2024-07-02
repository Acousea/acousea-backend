from abc import ABC, abstractmethod

from core.iclisten.domain.communicator.get_device_info_response import GetDeviceInfoResponse
from core.iclisten.domain.iclisten_device_info_read_model import ICListenDeviceInfoReadModel
from core.iclisten.domain.job_setup_read_model import JobSetupReadModel
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel


class ICListenRepository(ABC):
    @abstractmethod
    def get_device_info(self) -> ICListenDeviceInfoReadModel:
        pass

    @abstractmethod
    def get_job_setup(self) -> JobSetupReadModel:
        pass

    @abstractmethod
    def get_latest_stats(self, limit: int = 5) -> RecordingStatsReadModel:
        pass

    @abstractmethod
    def add_device_info(self, device_info: GetDeviceInfoResponse) -> None:
        pass


