from abc import ABC, abstractmethod

from core.iclisten.domain.communicator.get_pam_device_info_response import GetPAMDeviceInfoCommunicationResponse
from core.iclisten.domain.pam_system_logging_config_read_model import PAMDeviceLoggingConfigReadModel
from core.iclisten.domain.pam_system_status_info_read_model import PAMDeviceStatusReadModel
from core.iclisten.domain.pam_system_streaming_config_read_model import PAMDeviceStreamingConfigReadModel
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel


class PAMSystemRepository(ABC):
    @abstractmethod
    def get_pam_device_status_info(self) -> PAMDeviceStatusReadModel:
        pass

    @abstractmethod
    def get_logging_config(self) -> PAMDeviceLoggingConfigReadModel:
        pass

    @abstractmethod
    def get_streaming_config(self) -> PAMDeviceStreamingConfigReadModel:
        pass

    @abstractmethod
    def get_latest_recording_stats(self, limit: int = 5) -> RecordingStatsReadModel:
        pass

    @abstractmethod
    def add_pam_device_status_info(self, device_info: GetPAMDeviceInfoCommunicationResponse) -> None:
        pass

    @abstractmethod
    def get_pam_device_logging_config(self) -> PAMDeviceLoggingConfigReadModel:
        pass

    @abstractmethod
    def get_pam_device_streaming_config(self) -> PAMDeviceStreamingConfigReadModel:
        pass


