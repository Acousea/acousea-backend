class OperationCode:
    PING = '0'
    ERROR = '1'
    GET_DEVICE_INFO = 'E'
    CHANGE_OP_MODE = 'C'
    SUMMARY_REPORT = 'S'
    SUMMARY_SIMPLE_REPORT = 's'


    @staticmethod
    def to_int(code: str) -> int:
        return ord(code)
