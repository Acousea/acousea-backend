from abc import ABC, abstractmethod

from data_backend.device.info.domain.device_info_read_model import DeviceInfoReadModel


class DeviceInfoQueryRepository(ABC):

    @abstractmethod
    def get_all(self) -> DeviceInfoReadModel:
        pass
