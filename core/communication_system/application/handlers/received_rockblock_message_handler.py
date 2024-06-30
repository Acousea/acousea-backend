from typing import ClassVar, List

from fastapi import WebSocket

from core.communication_system.domain.events.received_rockblock_message_event import ReceivedRockBlockMessagePayload
from core.shared.application.event_handler import EventHandler


class ReceivedRockBlockMessageEventHandler(EventHandler[ReceivedRockBlockMessagePayload]):
    event_name: ClassVar[str] = "@rockblock/message_received"

    def __init__(self, client_list: List[WebSocket]):
        self.client_list = client_list

    async def handle(self, payload: ReceivedRockBlockMessagePayload):
        print("Handling event @rockblock/message_received")
        # TODO: Here we must send the message to the client
        for client in self.client_list:
            message_json = payload.message.model_dump(
                exclude={"id"}
            )
            print("Message JSON: ", message_json)
            await client.send_json(message_json)

        print("Message sent to all clients")
