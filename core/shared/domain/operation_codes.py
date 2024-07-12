class OperationCode:
    PING: chr = '0'
    ERROR: chr = '1'
    GET_PAM_DEVICE_INFO: chr = 'E'
    GET_PAM_DEVICE_STREAMING_CONFIG: chr = 'r'
    SET_PAM_DEVICE_STREAMING_CONFIG: chr = 'R'
    GET_PAM_DEVICE_LOGGING_CONFIG = 'l'
    SET_PAM_DEVICE_LOGGING_CONFIG = 'L'
    CHANGE_OP_MODE: chr = 'O'
    SUMMARY_REPORT: chr = 'S'
    SUMMARY_SIMPLE_REPORT: chr = 's'

    @staticmethod
    def to_int(code: chr) -> int:
        return ord(code)


if __name__ == "__main__":
    print(OperationCode.GET_PAM_DEVICE_INFO)
    print(OperationCode.to_int(OperationCode.GET_PAM_DEVICE_INFO))
