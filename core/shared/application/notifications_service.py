from enum import Enum
from typing import List

from starlette.websockets import WebSocket


class NotificationType(Enum):
    INFO = 'info'
    SUCCESS = 'success'
    ERROR = 'error'
    WARNING = 'warning'


class Notification:
    def __init__(self, message: str, notification_type: NotificationType = NotificationType.INFO):
        self.message = message
        self.type = notification_type

    def model_dump(self):
        return {
            "message": self.message,
            "type": self.type.value
        }


class NotificationService:
    """
    This class will store an array of WebSocket clients and will be
    in charge of sending notifications to them.
    """

    def __init__(self):
        self.client_list: List[WebSocket] = []

    async def __send_notification(self, notification: Notification):
        for client in self.client_list:
            await client.send_json(notification.model_dump())

    async def send_success_notification(self, message: str):
        await self.__send_notification(Notification(message, NotificationType.SUCCESS))

    async def send_error_notification(self, message: str):
        await self.__send_notification(Notification(message, NotificationType.ERROR))

    async def send_warning_notification(self, message: str):
        await self.__send_notification(Notification(message, NotificationType.WARNING))

    async def send_info_notification(self, message: str):
        await self.__send_notification(Notification(message, NotificationType.INFO))

    def add_client(self, client):
        self.client_list.append(client)

    def remove_client(self, client):
        self.client_list.remove(client)

    def get_clients(self):
        return self.client_list
