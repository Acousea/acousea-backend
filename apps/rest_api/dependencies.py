from typing import List

from fastapi import WebSocket

from core.communication_system.application.handlers.drifter_simple_report_response_handler import DrifterSimpleReportResponseEventHandler
from core.communication_system.application.handlers.localizer_simple_report_response_handler import LocalizerSimpleReportResponseEventHandler
from core.communication_system.application.handlers.received_rockblock_message_handler import ReceivedRockBlockMessageNotifierEventHandler
from core.communication_system.infrastructure.communication_system_client import \
    CommunicationSystemClient
from core.communication_system.infrastructure.communicator.iridium_communicator import IridiumCommunicator
from core.communication_system.infrastructure.communicator.serial_communicator import SerialCommunicator
from core.communication_system.infrastructure.rockblock_messages_repository import RockBlockMessagesRepository
from core.communication_system.infrastructure.sqlite_communication_system_query_repository import SQLiteCommunicationSystemQueryRepository
from core.iclisten.application.handlers.update_iclisten_device_info_event_handler import UpdateICListenDeviceInfoEventHandler
from core.iclisten.application.ports.iclisten_client import ICListenClient
from core.iclisten.infrastructure.sqlite_iclisten_repository import SQLiteICListenRepository
from core.shared.application.notifications_service import NotificationService
from core.shared.domain.db import DBManager
from core.shared.infrastructure.mock_event_bus import InMemoryEventBus
from core.surface_fields.infrastructure.NDFSurfaceFields2DSQueryRepository import \
    NDFSurfaceFields2DSQueryRepository

surface_fields_query_repository = NDFSurfaceFields2DSQueryRepository(
    nc_file_path="../../resources/netCDF_files/rtofs_glo_2ds_f087_prog.nc"
)

serial_communicator = SerialCommunicator(
    device="COM4",
    baud_rate=9600,
    timeout=3.0
)
iridium_communicator = IridiumCommunicator()

selected_communicator = iridium_communicator

# ----------------- websockets -----------------
clients: List[WebSocket] = []
notification_service = NotificationService()

# ----------------- SQLiteDatabase -----------------
db_manager = DBManager()
session = next(db_manager.get_db())

rockblock_messages_repository = RockBlockMessagesRepository(db=session)

# ----------------- ICListen -----------------
iclisten_query_repository = SQLiteICListenRepository(db=session)
iclisten_client = ICListenClient(communicator=selected_communicator)

# ----------------- Communication System -----------------
comm_system_query_repository = SQLiteCommunicationSystemQueryRepository(db=session)
comm_system_request_handler = CommunicationSystemClient(
    communicator=selected_communicator
)

# ----------------- Event Handlers -----------------
rockblock_message_event_handler = ReceivedRockBlockMessageNotifierEventHandler(
    notification_service=notification_service
)
update_iclisten_device_info_event_handler = UpdateICListenDeviceInfoEventHandler(
    notification_service=notification_service,
    repository=iclisten_query_repository
)

localizer_simple_report_response_event_handler = LocalizerSimpleReportResponseEventHandler(
    notification_service=notification_service,
    repository=comm_system_query_repository
)

drifter_simple_report_response_event_handler = DrifterSimpleReportResponseEventHandler(
    notification_service=notification_service,
    repository=comm_system_query_repository
)

# ----------------- Event Bus -----------------
event_bus = InMemoryEventBus()
event_bus.subscribe(
    handler=rockblock_message_event_handler
)
event_bus.subscribe(
    handler=update_iclisten_device_info_event_handler
)
event_bus.subscribe(
    handler=localizer_simple_report_response_event_handler
)
event_bus.subscribe(
    handler=drifter_simple_report_response_event_handler
)
