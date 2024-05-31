from abc import ABC, abstractmethod


class StorageService(ABC):
    @abstractmethod
    def download_latest(self) -> None:
        pass

    @abstractmethod
    def get_latest(self) -> str:
        pass

    @abstractmethod
    def get_all(self) -> list[str]:
        pass