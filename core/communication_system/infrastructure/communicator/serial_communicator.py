import asyncio
import threading
import time

import serial

from core.communication_system.application.ports.communicator import Communicator
from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.communication_system.domain.communicator.communication_response import CommunicationResponse
from core.communication_system.domain.communicator.communication_result import CommunicationResult, CommunicationStatus
from core.communication_system.domain.events.received_communication_response_event import ReceivedCommunicationResponseEvent, \
    CommunicationResponseEventPayload
from core.communication_system.infrastructure.request_logger_service import CommunicationRequestLoggerService
from core.shared.application.event_bus import EventBus
from core.shared.domain.address import Address


class SerialCommunicator(Communicator):
    def __init__(self, device, event_bus: EventBus, logger: CommunicationRequestLoggerService, baud_rate: int = 9600, timeout: float = 4.0):
        super().__init__("Serial Communicator")
        self.serial = None
        self.device = device
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.event_bus = event_bus
        self.logger = logger
        self.monitoring_thread = None
        self.monitoring = False

    def initialize(self):
        self.serial = serial.Serial(self.device,
                                    baudrate=self.baud_rate,
                                    timeout=self.timeout,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS
                                    )
        self.start_monitoring()

    def flush_communication_request_queue(self, localizer: bool, drifter: bool) -> CommunicationResult:
        self.serial.flushInput()
        self.serial.flushOutput()
        return CommunicationResult(CommunicationStatus.SUCCESS, message="Communication request queue flushed")

    def send_request(self, request: CommunicationRequest) -> CommunicationResult:
        try:
            self.logger.log_request(request)
        except Exception as unresolved_request_for_this_op_code_still_available:
            raise unresolved_request_for_this_op_code_still_available

        if self.serial is None:
            self.initialize()

        try:
            print("Sending request (as bytes):", request)
            self.serial.write(request.encode())
            return CommunicationResult(CommunicationStatus.SUCCESS, message="Message sent successfully")
        except Exception as e:
            return CommunicationResult(CommunicationStatus.FAILED, message=str(e))

    def start_monitoring(self):
        if self.monitoring_thread is None:
            self.monitoring = True
            self.monitoring_thread = threading.Thread(target=self.run_monitor_serial_port)
            self.monitoring_thread.start()

    def run_monitor_serial_port(self):
        asyncio.run(self.monitor_serial_port())

    async def monitor_serial_port(self):
        while self.monitoring:
            try:
                if self.serial.in_waiting > 0:
                    header = self.serial.read(4)
                    if header and len(header) == 4 and header[0] == 0x20:
                        response_length = header[3]
                        response_packet: bytes = header + self.serial.read(response_length)
                        self.print_response_packet(response_packet)
                        await self.handle_response(response_packet)
            except Exception as e:
                print(f"Error while reading from serial port: {e}")
            time.sleep(0.1)  # Avoid busy waiting

    async def handle_response(self, response_packet: bytes):
        try:
            communication_response = CommunicationResponse(response_packet)
            if communication_response.recipient_address != Address.BACKEND:
                print("This response is not for the backend")
                return
            print("Serial Communicator received response:", communication_response)
            received_communication_response_event = ReceivedCommunicationResponseEvent(
                payload=CommunicationResponseEventPayload(
                    opcode=communication_response.opcode,
                    sender_address=communication_response.sender_address,
                    recipient_address=communication_response.recipient_address,
                    response=communication_response.response
                )
            )
            await self.event_bus.notify_all([received_communication_response_event])
        except Exception as e:
            print(f"Error handling response: {e}")

    def close(self):
        self.monitoring = False
        if self.monitoring_thread is not None:
            self.monitoring_thread.join()
        if self.serial is not None:
            self.serial.close()

    @staticmethod
    def print_response_packet(response_packet):
        packet_str = " ".join([f"{byte:02X}" for byte in response_packet])
        print(f"Received response packet: {packet_str}")
        pass
