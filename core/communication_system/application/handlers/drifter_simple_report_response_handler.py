from typing import ClassVar

from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.communication_system.domain.communicator.responses.drifter_simple_report_response import DrifterSimpleReportResponse
from core.communication_system.domain.events.received_communication_response_event import CommunicationResponseEventPayload
from core.shared.application.event_handler import EventHandler
from core.shared.application.notifications_service import NotificationService
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class DrifterSimpleReportResponseEventHandler(EventHandler[CommunicationResponseEventPayload]):
    event_name: ClassVar[str] = "@communication/received_response"

    def __init__(self, notification_service: NotificationService, repository: CommunicationSystemQueryRepository):
        self.notification_service = notification_service
        self.repository = repository

    async def handle(self, payload: CommunicationResponseEventPayload):
        print("-------Handling event @communication/received_response-------")
        if payload.opcode != OperationCode.to_int(OperationCode.SUMMARY_SIMPLE_REPORT):
            print("DrifterSimpleReportResponseEventHandler: Operation code is not SUMMARY_SIMPLE_REPORT, ignoring event")
            return

        if payload.sender_address != Address.DRIFTER:
            print("DrifterSimpleReportResponseEventHandler: Address is not DRIFTER, ignoring event")
            return

        drifter_simple_report_response = DrifterSimpleReportResponse(
            payload.response
        )

        self.repository.store_simple_report_drifter_device_info(
            drifter_simple_report_response
        )
        # Send a success notification to the client
        await self.notification_service.send_success_notification(
            message="Drifter device info updated"
        )
        print("Message sent to all clients")
