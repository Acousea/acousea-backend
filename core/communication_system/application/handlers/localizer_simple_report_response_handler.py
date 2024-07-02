from typing import ClassVar

from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.communication_system.domain.communicator.responses.localizer_simple_report_response import LocalizerSimpleReportResponse
from core.communication_system.domain.events.received_communication_response_event import CommunicationResponseEventPayload
from core.shared.application.event_handler import EventHandler
from core.shared.application.notifications_service import NotificationService
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class LocalizerSimpleReportResponseEventHandler(EventHandler[CommunicationResponseEventPayload]):
    event_name: ClassVar[str] = "@communication/received_response"

    def __init__(self, notification_service: NotificationService, repository: CommunicationSystemQueryRepository):
        self.notification_service = notification_service
        self.repository = repository

    async def handle(self, payload: CommunicationResponseEventPayload):
        print("-------Handling event @communication/received_response-------")
        if payload.opcode != OperationCode.to_int(OperationCode.SUMMARY_SIMPLE_REPORT):
            print("LocalizerSimpleReportResponseEventHandler: Operation code is not SUMMARY_SIMPLE_REPORT, ignoring event")
            return

        if payload.sender_address != Address.LOCALIZER:
            print("LocalizerSimpleReportResponseEventHandler: Address is not LOCALIZER, ignoring event")
            return

        localizer_simple_report_response = LocalizerSimpleReportResponse(
            payload.response
        )

        self.repository.store_simple_report_localizer_device_info(
            localizer_simple_report_response
        )
        # Send a success notification to the client
        await self.notification_service.send_info_notification(
            message="Localizer device info updated"
        )
        print("Message sent to all clients")
