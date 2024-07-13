from typing import ClassVar

from core.communication_system.domain.communicator.responses.error_response import ErrorCommunicationResponse
from core.communication_system.domain.events.received_communication_response_event import CommunicationResponseEventPayload
from core.communication_system.infrastructure.request_logger_service import CommunicationRequestLoggerService
from core.shared.application.event_handler import EventHandler
from core.shared.application.notifications_service import NotificationService
from core.shared.domain.operation_codes import OperationCode


class ErrorCommunicationResponseEventHandler(EventHandler[CommunicationResponseEventPayload]):
    event_name: ClassVar[str] = "@communication/received_response"

    def __init__(self, notification_service: NotificationService, request_logger_service: CommunicationRequestLoggerService):
        self.notification_service = notification_service
        self.request_logger_service = request_logger_service

    async def handle(self, payload: CommunicationResponseEventPayload):
        print("-------ErrorCommunicationResponseEventHandler: Handling event @communication/received_response-------")
        # Check if the operation code is an ERROR
        if payload.opcode != OperationCode.to_int(OperationCode.ERROR):
            print("UpdateICListenDeviceInfoEventHandler: Operation code is not ERROR, ignoring event")
            return

        # Create the error response object
        error_response = ErrorCommunicationResponse(payload.response)

        print("Error Communication Response:")
        print(error_response)

        # Mark resolved request
        self.request_logger_service.resolve_request(
            chr(error_response.error_op_code),
            payload.sender_address
        )

        await self.notification_service.send_error_notification(
            message=error_response.get_error_description()
        )
        print("Message sent to all clients")
