from typing import List

import serial.tools.list_ports
from pydantic import BaseModel

from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class COMDeviceReadModel(BaseModel):
    device: str
    name: str
    description: str
    serial_number: str


class AvailableCOMDevicesHttpResponse(BaseModel):
    devices: List[COMDeviceReadModel]


class GetAvailableCOMDevicesHttpRequest(HttpRequest[None, AvailableCOMDevicesHttpResponse]):

    def execute(self, params: None = None) -> HttpResponse[AvailableCOMDevicesHttpResponse]:
        ports = serial.tools.list_ports.comports()
        devices: List[COMDeviceReadModel] = [
            COMDeviceReadModel(
                device=port.device,
                name=port.name,
                description=port.description,
                serial_number=port.serial_number
            ) for port in ports]

        if len(ports) > 0:
            return HttpResponse.ok(
                AvailableCOMDevicesHttpResponse(
                    devices=devices
                )
            )
        return HttpResponse.fail(message="No serial devices found")
