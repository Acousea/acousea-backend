class OperationMode:
    KEEP_CURRENT_MODE = 0
    LAUNCHING_MODE = 1
    WORKING_MODE = 2
    RECOVERY_MODE = 3

    # Method to check if an operation mode is valid
    @staticmethod
    def is_valid_mode(op_mode: int) -> bool:
        return op_mode in [OperationMode.KEEP_CURRENT_MODE, OperationMode.LAUNCHING_MODE, OperationMode.WORKING_MODE,
                           OperationMode.RECOVERY_MODE]
