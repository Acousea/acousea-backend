from core.communication_system.domain.OperationMode import OperationMode
from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class DrifterChangeOpModeResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        self.acknowledged = bool(self.data[0])
        if not OperationMode.is_valid_mode(self.data[1]):
            raise ValueError(f'Invalid operation mode: {self.data[1]}')
        self.op_mode = int(self.data[1])

    def __str__(self):
        return f'DrifterChangeOpModeResponse (acknowledged={self.acknowledged}, op_mode={self.op_mode})'

    def __repr__(self):
        return self.__str__()

