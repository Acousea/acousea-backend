from typing import ClassVar

from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.communication_system.domain.communicator.responses.localizer_change_op_mode_response import LocalizerChangeOpModeResponse
from core.communication_system.domain.events.received_communication_response_event import CommunicationResponseEventPayload
from core.communication_system.infrastructure.request_logger_service import CommunicationRequestLoggerService
from core.shared.application.event_handler import EventHandler
from core.shared.application.notifications_service import NotificationService
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class LocalizerChangeOpModeResponseEventHandler(EventHandler[CommunicationResponseEventPayload]):
    event_name: ClassVar[str] = "@communication/received_response"

    def __init__(self, notification_service: NotificationService,
                 comm_system_query_repository: CommunicationSystemQueryRepository,
                 request_logger_service: CommunicationRequestLoggerService
                 ):
        self.notification_service = notification_service
        self.repository = comm_system_query_repository
        self.request_logger_service = request_logger_service

    async def handle(self, payload: CommunicationResponseEventPayload):
        print("-------LocalizerChangeOpModeResponseEventHandler: Handling event @communication/received_response-------")
        if payload.opcode != OperationCode.to_int(OperationCode.CHANGE_OP_MODE):
            print("LocalizerChangeOpModeResponseEventHandler: Operation code is not CHANGE_OP_MODE, ignoring event")
            return

        if payload.sender_address != Address.LOCALIZER:
            print("LocalizerChangeOpModeResponseEventHandler: Sender Address is not LOCALIZER, ignoring event")
            return

        localizer_op_mode_response = LocalizerChangeOpModeResponse(
            payload.response
        )

        self.repository.store_localizer_op_mode(
            localizer_op_mode_response.op_mode
        )

        self.request_logger_service.resolve_request(
            OperationCode.CHANGE_OP_MODE,
            Address.LOCALIZER
        )

        # Send a success notification to the client
        await self.notification_service.send_success_notification(
            message="Localizer device operation mode updated"
        )

        print("Message sent to all clients")
