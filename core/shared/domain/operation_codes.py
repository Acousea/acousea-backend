class OperationCode:
    PING: chr = '0'
    ERROR: chr = '1'
    GET_DEVICE_INFO: chr = 'E'
    CHANGE_OP_MODE: chr = 'C'
    SUMMARY_REPORT: chr = 'S'
    SUMMARY_SIMPLE_REPORT: chr = 's'

    @staticmethod
    def to_int(code: chr) -> int:
        return ord(code)


if __name__ == "__main__":
    print(OperationCode.GET_DEVICE_INFO)
    print(OperationCode.to_int(OperationCode.GET_DEVICE_INFO))
