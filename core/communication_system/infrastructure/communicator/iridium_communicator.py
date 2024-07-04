import os
from enum import Enum

from dotenv import load_dotenv

from core.communication_system.application.ports.communicator import Communicator
from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.communication_system.domain.communicator.communication_result import CommunicationResult, CommunicationStatus
from core.communication_system.infrastructure.request_logger_service import CommunicationRequestLoggerService
from core.shared.domain.address import Address

import requests

class IridiumErrorCode(Enum):
    INVALID_LOGIN_CREDENTIALS = 10
    NO_ROCKBLOCK_FOUND = 11
    NO_LINE_RENTAL = 12
    INSUFFICIENT_CREDIT = 13
    DECODE_HEX_DATA_ERROR = 14
    DATA_TOO_LONG = 15
    NO_DATA = 16
    SYSTEM_ERROR = 99

    @classmethod
    def get_description(cls, code):
        descriptions = {
            cls.INVALID_LOGIN_CREDENTIALS: "Invalid login credentials",
            cls.NO_ROCKBLOCK_FOUND: "No RockBLOCK with this IMEI found on your account",
            cls.NO_LINE_RENTAL: "RockBLOCK has no line rental",
            cls.INSUFFICIENT_CREDIT: "Your account has insufficient credit",
            cls.DECODE_HEX_DATA_ERROR: "Could not decode hex data",
            cls.DATA_TOO_LONG: "Data too long",
            cls.NO_DATA: "No data",
            cls.SYSTEM_ERROR: "System Error"
        }
        return descriptions.get(code, "Unknown error code")


class IridiumCommunicator(Communicator):
    def __init__(self, logger: CommunicationRequestLoggerService):
        super().__init__("Iridium Communicator")
        self.logger = logger
        load_dotenv()
        self.base_url = "https://rockblock.rock7.com/rockblock/MT"
        self.username = os.getenv("IRIDIUM_USERNAME")
        self.password = os.getenv("IRIDIUM_PASSWORD")
        self.localizer_imei = os.getenv("LOCALIZER_IMEI")
        self.localizer_serial = os.getenv("LOCALIZER_SERIAL")
        self.drifter_imei = os.getenv("DRIFTER_IMEI")
        self.drifter_serial = os.getenv("DRIFTER_SERIAL")

    def initialize(self):
        pass

    def get_imei(self, communication_request: CommunicationRequest):
        if communication_request.is_recipient_address(Address.LOCALIZER):
            return self.localizer_imei
        elif communication_request.is_recipient_address(Address.DRIFTER) or communication_request.is_recipient_address(Address.PI3):
            return self.drifter_imei
        else:
            raise ValueError("Invalid recipient address")

    def flush_communication_request_queue(self, localizer: bool, drifter: bool) -> CommunicationResult:
        if not localizer and not drifter:
            raise ValueError("At least one of the localizer or drifter must be flushed")

        localizer_response, drifter_response = None, None
        if localizer:
            url = f"{self.base_url}?imei={self.localizer_imei}&username={self.username}&password={self.password}&flush=yes"
            headers = {"accept": "text/plain"}
            response = requests.post(url, headers=headers)
            localizer_response = self.handle_response(response.text)

        if drifter:
            url = f"{self.base_url}?imei={self.drifter_imei}&username={self.username}&password={self.password}&flush=yes"
            headers = {"accept": "text/plain"}
            response = requests.post(url, headers=headers)
            drifter_response = self.handle_response(response.text)

        if (localizer_response and localizer_response.status == CommunicationStatus.SUCCESS) and (
                drifter_response and drifter_response.status == CommunicationStatus.SUCCESS):
            return CommunicationResult(CommunicationStatus.SUCCESS, message="Message queue flushed successfully")
        else:
            if localizer_response and localizer_response.status == CommunicationStatus.FAILED and drifter_response and drifter_response.status == CommunicationStatus.FAILED:
                return CommunicationResult(CommunicationStatus.FAILED, message="Failed to flush both localizer and drifter message queues")
            if localizer_response and localizer_response.status == CommunicationStatus.FAILED:
                return CommunicationResult(CommunicationStatus.FAILED, message="Failed to flush drifter message queue")
            if drifter_response and drifter_response.status == CommunicationStatus.FAILED:
                return CommunicationResult(CommunicationStatus.FAILED, message="Failed to flush localizer message queue")

    def send_request(self, communication_request: CommunicationRequest) -> CommunicationResult:
        try:
            self.logger.log_request(communication_request)
        except Exception as unresolved_request_for_this_op_code_still_available:
            raise unresolved_request_for_this_op_code_still_available

        imei = self.get_imei(communication_request)

        url = f"{self.base_url}?imei={imei}&username={self.username}&password={self.password}&data={communication_request.encode_str()}"

        print("URL:", url)
        headers = {"accept": "text/plain"}
        # response = requests.post(url, headers=headers)
        # return self.handle_response(response.text)
        # return CommunicationResult(CommunicationStatus.FAILED, message="Failed to send message", error_code=IridiumErrorCode.SYSTEM_ERROR.value)
        return CommunicationResult(CommunicationStatus.SUCCESS, message="Message sent successfully")

    @staticmethod
    def handle_response(response_text: str) -> CommunicationResult:
        parts = response_text.split(',')
        status = parts[0]
        if status == "OK":
            mt_id = parts[1]
            return CommunicationResult(CommunicationStatus.SUCCESS, message="Message sent successfully", res_id=mt_id)
        elif status == "FAILED":
            error_code = int(parts[1])
            error_description = parts[2]
            return CommunicationResult(CommunicationStatus.FAILED, message=error_description, error_code=error_code)
        else:
            return CommunicationResult(CommunicationStatus.UNKNOWN, message="Unknown error")

    def close(self):
        pass
