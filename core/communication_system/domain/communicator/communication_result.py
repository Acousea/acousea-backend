from enum import Enum

from pydantic import BaseModel


class CommunicationResultHttpResponse(BaseModel):
    status: str
    message: str


class CommunicationStatus(Enum):
    SUCCESS = "OK"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class CommunicationResult:
    def __init__(self, status: CommunicationStatus, message: str, res_id: str = None, error_code: int = None):
        self.id = res_id
        self.status = status
        self.error_code = error_code
        self.message = message

    def __str__(self):
        if self.status == CommunicationStatus.SUCCESS:
            return f"Status: {self.status.value}, Message ID: {self.id}, Message: {self.message}"
        elif self.status == CommunicationStatus.FAILED:
            return f"Status: {self.status.value}, Error Code: {self.error_code}, Error Message: {self.message}"
        else:
            return f"Status: {self.status.value}, Message: {self.message}"
