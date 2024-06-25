from core.shared.domain.communicator.communication_request import CommunicationRequest
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class ChangeLocalizerOpModeRequest(CommunicationRequest):

    def __init__(self, op_mode: int):
        # Static field containing the payload of the request
        self.content = bytes([op_mode])
        super().__init__(OperationCode.CHANGE_OP_MODE, Address.LOCALIZER, self.content)

    def __str__(self):
        return f'ChangeLocalizerOpModeRequest{super().__str__()}'

    def __repr__(self):
        return f'ChangeLocalizerOpModeRequest{super().__repr__()}'

