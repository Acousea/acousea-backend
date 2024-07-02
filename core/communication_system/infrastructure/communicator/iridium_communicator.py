import os
from enum import Enum

import requests
from dotenv import load_dotenv

from core.communication_system.application.ports.communicator import Communicator
from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.communication_system.domain.communicator.communication_result import CommunicationResult, CommunicationStatus
from core.communication_system.domain.communicator.requests.ping_drifter_request import PingDrifterRequest
from core.shared.domain.address import Address


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
    def __init__(self):
        load_dotenv()
        self.base_url = "https://rockblock.rock7.com/rockblock/MT"
        self.username = os.getenv("IRIDIUM_USERNAME")
        self.password = os.getenv("IRIDIUM_PASSWORD")
        self.localizer_imei = os.getenv("LOCALIZER_IMEI")
        self.localizer_serial = os.getenv("LOCALIZER_SERIAL")
        self.drifter_imei = os.getenv("DRIFTER_IMEI")
        self.drifter_serial = os.getenv("DRIFTER_SERIAL")

    def send_request(self, communication_request: CommunicationRequest) -> CommunicationResult:
        imei = self.get_imei(communication_request)

        url = f"{self.base_url}?imei={imei}&username={self.username}&password={self.password}&data={communication_request.encode_str()}"
        if communication_request.flush:
            url += "&flush=yes"

        print("URL:", url)
        headers = {"accept": "text/plain"}
        # response = requests.post(url, headers=headers)
        # return self.handle_response(response.text)
        # return CommunicationResult(CommunicationStatus.FAILED, message="Failed to send message", error_code=IridiumErrorCode.SYSTEM_ERROR.value)
        return CommunicationResult(CommunicationStatus.SUCCESS, message="Message sent successfully")

    def get_imei(self, communication_request: CommunicationRequest):
        if communication_request.is_recipient_address(Address.LOCALIZER):
            return self.localizer_imei
        elif communication_request.is_recipient_address(Address.DRIFTER) or communication_request.is_recipient_address(Address.PI3):
            return self.drifter_imei
        else:
            raise ValueError("Invalid recipient address")

    @staticmethod
    def handle_response(response_text: str) -> CommunicationResult:
        parts = response_text.split(',')
        status = parts[0]
        if status == "OK":
            mt_id = parts[1]
            return CommunicationResult(CommunicationStatus.SUCCESS, message="Message sent successfully", id=mt_id)
        elif status == "FAILED":
            error_code = int(parts[1])
            error_description = parts[2]
            return CommunicationResult(CommunicationStatus.FAILED, message=error_description, error_code=error_code)
        else:
            return CommunicationResult(CommunicationStatus.UNKNOWN, message="Unknown error")

    def close(self):
        pass


if __name__ == "__main__":
    communicator = IridiumCommunicator()
    print("Username:", communicator.username)
    print("Password:", communicator.password)
    print("Localizer IMEI:", communicator.localizer_imei)
    print("Localizer Serial:", communicator.localizer_serial)
    print("Drifter IMEI:", communicator.drifter_imei)
    print("Drifter Serial:", communicator.drifter_serial)

    # request = CommunicationRequest("T", Address.LOCALIZER, b"Hello, World!")
    request = PingDrifterRequest()
    communicator.send_request(request)
