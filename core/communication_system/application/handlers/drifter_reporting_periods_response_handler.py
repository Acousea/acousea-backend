from typing import ClassVar

from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.communication_system.domain.communicator.responses.drifter_reporting_periods_response import DrifterReportingPeriodsResponse
from core.communication_system.domain.events.received_communication_response_event import CommunicationResponseEventPayload
from core.communication_system.infrastructure.request_logger_service import CommunicationRequestLoggerService
from core.shared.application.event_handler import EventHandler
from core.shared.application.notifications_service import NotificationService
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class DrifterReportingPeriodsResponseEventHandler(EventHandler[CommunicationResponseEventPayload]):
    event_name: ClassVar[str] = "@communication/received_response"

    def __init__(self, notification_service: NotificationService,
                 comm_system_query_repository: CommunicationSystemQueryRepository,
                 request_logger_service: CommunicationRequestLoggerService
                 ):
        self.notification_service = notification_service
        self.repository = comm_system_query_repository
        self.request_logger_service = request_logger_service

    async def handle(self, payload: CommunicationResponseEventPayload):
        print("-------DrifterReportingPeriodsResponseEventHandler: Handling event @communication/received_response-------")
        if (payload.opcode != OperationCode.to_int(OperationCode.SET_REPORTING_PERIODS) and
                payload.opcode != OperationCode.to_int(OperationCode.GET_REPORTING_PERIODS)):
            print("DrifterReportingPeriodsResponseEventHandler: Operation code is not SET_REPORTING_PERIODS or GET_REPORTING_PERIODS, ignoring event")
            return

        if payload.sender_address != Address.DRIFTER:
            print("DrifterReportingPeriodsResponseEventHandler: Sender Address is not DRIFTER, ignoring event")
            return

        drifter_reporting_periods_response = DrifterReportingPeriodsResponse(
            payload.response
        )

        self.repository.store_drifter_reporting_periods(
            drifter_reporting_periods_response
        )

        if payload.opcode == OperationCode.to_int(OperationCode.SET_REPORTING_PERIODS):
            self.request_logger_service.resolve_request(
                OperationCode.SET_REPORTING_PERIODS,
                Address.DRIFTER
            )

            # Send a success notification to the client
            await self.notification_service.send_success_notification(
                message="Drifter reporting periods set"
            )
        else:
            self.request_logger_service.resolve_request(
                OperationCode.GET_REPORTING_PERIODS,
                Address.DRIFTER
            )

            # Send a success notification to the client
            await self.notification_service.send_success_notification(
                message="Drifter  reporting periods retrieved"
            )

        print("Message sent to all clients")
