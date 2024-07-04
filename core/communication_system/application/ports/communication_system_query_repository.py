from abc import ABC, abstractmethod

from core.communication_system.domain.communicator.responses.drifter_simple_report_response import DrifterSimpleReportResponse
from core.communication_system.domain.communicator.responses.localizer_simple_report_response import \
    LocalizerSimpleReportResponse


class CommunicationSystemQueryRepository(ABC):
    @abstractmethod
    def get_drifter_op_mode(self) -> int:
        pass

    @abstractmethod
    def get_localizer_op_mode(self) -> int:
        pass

    @abstractmethod
    def store_drifter_op_mode(self, op_mode: int):
        pass

    @abstractmethod
    def store_localizer_op_mode(self, op_mode: int):
        pass

    @abstractmethod
    def get_drifter_location(self) -> tuple[float, float] | None:
        pass

    @abstractmethod
    def get_localizer_location(self) -> tuple[float, float] | None:
        pass

    @abstractmethod
    def store_simple_report_drifter_device_info(self, drifter_info: DrifterSimpleReportResponse):
        pass

    @abstractmethod
    def store_simple_report_localizer_device_info(self, localizer_info: LocalizerSimpleReportResponse):
        pass
