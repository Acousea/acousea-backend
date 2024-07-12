from typing import ClassVar

from core.communication_system.domain.events.received_rockblock_message_event import ReceivedRockBlockMessagePayload
from core.shared.application.event_handler import EventHandler
from core.shared.application.notifications_service import NotificationService


class ReceivedRockBlockMessageNotifierEventHandler(EventHandler[ReceivedRockBlockMessagePayload]):
    event_name: ClassVar[str] = "@rockblock/received_message"

    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    async def handle(self, payload: ReceivedRockBlockMessagePayload):
        print("======= ReceivedRockBlockMessageNotifierEventHandler: Handling event @rockblock/received_message")
        # Send a success notification to the client
        await self.notification_service.send_info_notification(
            message="New RockBlock message received"
        )
        print("Message sent to all clients")


