import serial.tools.list_ports
from pydantic import BaseModel

from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse
from core.shared.infrastructure.communicator.serial_communicator import SerialCommunicator
from apps.rest_api.dependencies import selected_communicator


class SetupDirectCommunicationParams(BaseModel):
    serial_number: str


class SetupDirectCommunicationHttpResponse(BaseModel):
    message: str


class SetupDirectCommunicationHttpRequest(
    HttpRequest[SetupDirectCommunicationParams, SetupDirectCommunicationHttpResponse]):

    def execute(self, params: SetupDirectCommunicationParams | None = None) -> HttpResponse[SetupDirectCommunicationHttpResponse]:
        if params is None:
            return HttpResponse.fail(message="You need to pass a usb device serial number")

        if self.update_selected_communicator(params.serial_number):
            return HttpResponse.ok(
                SetupDirectCommunicationHttpResponse(
                    message="Direct communication setup successful")
            )
        return HttpResponse.fail(message="No device found with the given serial number")

    @staticmethod
    def update_selected_communicator(serial_number) -> bool:
        global selected_communicator
        ports = serial.tools.list_ports.comports()
        # Print the previous selected communicator
        print("Previous selected communicator: ", selected_communicator.device)
        print("Ports: ", [(port.serial_number, port.name) for port in ports])
        for port in ports:
            if port.serial_number == serial_number:

                selected_communicator = SerialCommunicator(
                    device=port.device,
                    baud_rate=9600,
                    timeout=3.0
                )
                return True
        else:
            return False
