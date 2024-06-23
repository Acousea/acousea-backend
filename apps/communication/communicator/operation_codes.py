class OperationCode:
    PING = '0'
    ERROR = '1'
    GET_DEVICE_INFO = 'E'

    @staticmethod
    def to_int(code: str) -> int:
        return ord(code)
