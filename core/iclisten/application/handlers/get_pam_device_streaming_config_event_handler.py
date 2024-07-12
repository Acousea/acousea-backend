from typing import ClassVar

from core.communication_system.infrastructure.request_logger_service import CommunicationRequestLoggerService
from core.iclisten.application.ports.iclisten_repository import PAMSystemRepository
from core.iclisten.domain.communicator.get_pam_device_info_response import GetPAMDeviceInfoCommunicationResponse
from core.communication_system.domain.events.received_communication_response_event import CommunicationResponseEventPayload
from core.iclisten.domain.communicator.get_pam_device_streaming_config_response import GetPAMDeviceStreamingConfigCommunicationResponse
from core.shared.application.event_handler import EventHandler
from core.shared.application.notifications_service import NotificationService
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class GetPAMDeviceStreamingConfigEventHandler(EventHandler[CommunicationResponseEventPayload]):
    """
    This handler will check first for the operation code before it decides if
    it must handle the event or not.
    """
    event_name: ClassVar[str] = "@communication/received_response"

    def __init__(self, notification_service: NotificationService,
                 pam_system_repository: PAMSystemRepository,
                 request_logger_service: CommunicationRequestLoggerService):
        self.notification_service = notification_service
        self.repository = pam_system_repository
        self.request_logger_service = request_logger_service

    async def handle(self, payload: CommunicationResponseEventPayload):
        print("-------GetPAMDeviceStreamingConfigEventHandler: Handling event @communication/received_response")
        if payload.opcode != OperationCode.to_int(OperationCode.GET_PAM_DEVICE_STREAMING_CONFIG):
            print("GetPAMDeviceStreamingConfigEventHandler: Operation code is not GET_PAM_DEVICE_STREAMING_CONFIG, ignoring event")
            return

        if payload.sender_address != Address.PI3:
            print("GetPAMDeviceStreamingConfigEventHandler: Address is not PI3, ignoring event")
            return

        # Create the response object
        pam_device_streaming_config = GetPAMDeviceStreamingConfigCommunicationResponse(
            payload.response
        )

        print("PAM Device Streaming Config Response:")
        print(pam_device_streaming_config)

        # Decode the message data, store it in the repository
        self.repository.add_pam_device_streaming_config(
            pam_device_streaming_config
        )

        self.request_logger_service.resolve_request(
            OperationCode.GET_PAM_DEVICE_STREAMING_CONFIG,
            Address.PI3
        )

        # Send a success notification to the client
        await self.notification_service.send_success_notification(
            message="Streaming settings updated successfully",
        )

        print("Message sent to all clients")
