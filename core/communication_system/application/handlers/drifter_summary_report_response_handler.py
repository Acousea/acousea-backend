import asyncio
from typing import ClassVar

from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.communication_system.domain.communicator.responses.drifter_summary_report_response import DrifterSummaryReportResponse

from core.communication_system.domain.events.received_communication_response_event import CommunicationResponseEventPayload
from core.iclisten.application.ports.iclisten_repository import PAMSystemRepository
from core.shared.application.event_handler import EventHandler
from core.shared.application.notifications_service import NotificationService
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class DrifterSummaryReportResponseEventHandler(EventHandler[CommunicationResponseEventPayload]):
    event_name: ClassVar[str] = "@communication/received_response"

    def __init__(self, notification_service: NotificationService,
                 pam_system_repository: PAMSystemRepository,
                 communication_system_repository: CommunicationSystemQueryRepository):
        self.notification_service = notification_service
        self.comm_system_repository = communication_system_repository
        self.pam_system_repository = pam_system_repository

    async def handle(self, payload: CommunicationResponseEventPayload):
        print("-------DrifterSummaryReportResponseEventHandler: Handling event @communication/received_response-------")
        if payload.opcode != OperationCode.to_int(OperationCode.SUMMARY_REPORT):
            print("DrifterSummaryReportResponseEventHandler: Operation code is not SUMMARY_REPORT, ignoring event")
            return

        if payload.sender_address != Address.DRIFTER:
            print("DrifterSummaryReportResponseEventHandler: Address is not DRIFTER, ignoring event")
            return

        drifter_summary_report_response = DrifterSummaryReportResponse(
            payload.response
        )

        print("Drifter Summary Report Response:")
        print(drifter_summary_report_response)

        self.comm_system_repository.store_summary_report_drifter_device_info(
            drifter_summary_report_response
        )

        self.pam_system_repository.add_recording_stats_info(
            drifter_summary_report_response
        )

        self.pam_system_repository.update_pam_device_status_info(
            drifter_summary_report_response
        )

        # Send a success notification to the client
        # Send notifications using asyncio.gather to run them concurrently
        await asyncio.gather(
            await self.notification_service.send_info_notification(
                message="Summary report received"
            ),
            await self.notification_service.send_success_notification(
                message="Communication System Status and Recording Stats updated"
            )
        )

        print("Message sent to all clients")
