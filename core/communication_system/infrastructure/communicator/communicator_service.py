from typing import Type

import serial.tools.list_ports

from core.communication_system.application.ports.communicator import Communicator
from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.communication_system.domain.communicator.communication_result import CommunicationResult
from core.communication_system.infrastructure.communicator.iridium_communicator import IridiumCommunicator
from core.communication_system.infrastructure.communicator.serial_communicator import SerialCommunicator


class CommunicatorService:
    def __init__(self, serial_communicator: SerialCommunicator, iridium_communicator: IridiumCommunicator):
        self._serial_communicator = serial_communicator
        self._iridium_communicator = iridium_communicator
        self._selected_communicator: Communicator = self._serial_communicator # self._iridium_communicator
        self.selected_communicator.initialize()

    @property
    def selected_communicator(self) -> Communicator:
        return self._selected_communicator

    @selected_communicator.setter
    def selected_communicator(self, communicator_type: Type[Communicator]):
        if communicator_type == SerialCommunicator:
            self.close()
            self._serial_communicator.initialize()
            self._selected_communicator = self._serial_communicator
        elif communicator_type == IridiumCommunicator:
            self.close()
            self._selected_communicator = self._iridium_communicator
        else:
            raise ValueError("Invalid communicator type")

    def is_serial_communicator_selected(self) -> bool:
        return self._selected_communicator.name == self._serial_communicator.name

    def use_serial_communicator(self, serial_number: str | None = None) -> bool:
        if serial_number is not None:
            success = self.__update_serial_communicator(serial_number)
            if not success:
                return False
        self.selected_communicator = SerialCommunicator
        return True

    def __update_serial_communicator(self, serial_number: str) -> bool:
        ports = serial.tools.list_ports.comports()
        # Print the previous selected communicator
        for port in ports:
            if port.serial_number == serial_number:
                self._serial_communicator.device = port.device
                return True
        else:
            return False

    def use_iridium_communicator(self):
        self.selected_communicator = IridiumCommunicator

    def send_request(self, request: CommunicationRequest) -> CommunicationResult:
        return self._selected_communicator.send_request(request)

    def flush_communication_request_queue(self, localizer: bool, drifter: bool) -> CommunicationResult:
        return self._selected_communicator.flush_communication_request_queue(localizer, drifter)

    def close(self):
        self._selected_communicator.close()
