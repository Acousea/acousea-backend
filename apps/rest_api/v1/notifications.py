from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from apps.rest_api.dependencies import notification_service

router = APIRouter()


@router.websocket("/ws/notifications")
async def notifications_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    notification_service.add_client(websocket)
    print("New WebSocket accepted, notification_clients: ", len(notification_service.get_clients()))
    try:
        while True:
            data = await websocket.receive_text()
            # Do something with the data if needed
    except WebSocketDisconnect:
        notification_service.remove_client(websocket)
        print("WebSocket disconnected, notification_clients: ", len(notification_service.get_clients()))
