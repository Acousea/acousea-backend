from abc import ABC, abstractmethod

from data_backend.iclisten.domain.ICListenClient import ICListenClient
from data_backend.iclisten.domain.device_info_read_model import DeviceInfoReadModel


class ICListenRequestHandler(ABC):

    def __init__(self, iclisten_client: ICListenClient):
        self.iclisten_client = iclisten_client

    @abstractmethod
    def retrieve_device_info(self) -> DeviceInfoReadModel:
        pass

    @abstractmethod
    def job_setup(self) -> None:
        pass
