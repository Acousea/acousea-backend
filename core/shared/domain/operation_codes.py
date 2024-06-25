class OperationCode:
    PING = '0'
    ERROR = '1'
    GET_DEVICE_INFO = 'E'
    CHANGE_OP_MODE = 'C'

    @staticmethod
    def to_int(code: str) -> int:
        return ord(code)
