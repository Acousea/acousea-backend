from typing import ClassVar

from core.iclisten.application.ports.iclisten_repository import ICListenRepository
from core.iclisten.domain.communicator.get_device_info_response import GetDeviceInfoResponse
from core.communication_system.domain.events.received_communication_response_event import CommunicationResponseEventPayload
from core.shared.application.event_handler import EventHandler
from core.shared.application.notifications_service import NotificationService
from core.shared.domain.operation_codes import OperationCode


class UpdateICListenDeviceInfoEventHandler(EventHandler[CommunicationResponseEventPayload]):
    """
    This handler will check first for the operation code before it decides if
    it must handle the event or not.
    """
    event_name: ClassVar[str] = "@communication/received_response"

    def __init__(self, notification_service: NotificationService, repository: ICListenRepository):
        self.notification_service = notification_service
        self.repository = repository

    async def handle(self, response: CommunicationResponseEventPayload):
        print("Handling event @communication/received_response")
        if response.opcode != OperationCode.to_int(OperationCode.GET_DEVICE_INFO):
            print("UpdateICListenDeviceInfoEventHandler: Operation code is not GET_DEVICE_INFO, ignoring event")
            return
        # Decode the message data, store it in the repository
        self.repository.add_device_info(GetDeviceInfoResponse(response.response))

        # Send a success notification to the client
        await self.notification_service.send_success_notification(
            message="Device info updated successfully",
        )

        print("Message sent to all clients")
