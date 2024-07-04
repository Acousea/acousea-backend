class PreviousUnresolvedRequestException(Exception):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return f"[PreviousUnresolvedRequestException::Error{self.error_code}]: {self.message}"
        else:
            return self.message
