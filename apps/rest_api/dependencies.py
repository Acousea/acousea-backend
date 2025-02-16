from typing import List

from fastapi import WebSocket
from sqlalchemy.orm import Session

from core.communication_system.application.handlers.drifter_change_opmode_response_handler import DrifterChangeOpModeResponseEventHandler
from core.communication_system.application.handlers.drifter_reporting_periods_response_handler import DrifterReportingPeriodsResponseEventHandler
from core.communication_system.application.handlers.drifter_simple_report_response_handler import DrifterSimpleReportResponseEventHandler
from core.communication_system.application.handlers.drifter_summary_report_response_handler import DrifterSummaryReportResponseEventHandler
from core.communication_system.application.handlers.error_communication_response_handler import ErrorCommunicationResponseEventHandler
from core.communication_system.application.handlers.localizer_change_opmode_response_handler import LocalizerChangeOpModeResponseEventHandler
from core.communication_system.application.handlers.localizer_simple_report_response_handler import LocalizerSimpleReportResponseEventHandler
from core.communication_system.application.handlers.received_rockblock_message_handler import ReceivedRockBlockMessageNotifierEventHandler
from core.communication_system.domain.sqlalchemy.sql_communication_request_history_repository import SQLCommunicationRequestHistoryRepository
from core.communication_system.infrastructure.communication_system_client import CommunicationSystemClient
from core.communication_system.infrastructure.communicator.communicator_service import CommunicatorService
from core.communication_system.infrastructure.communicator.iridium_communicator import IridiumCommunicator
from core.communication_system.infrastructure.communicator.serial_communicator import SerialCommunicator
from core.communication_system.infrastructure.request_logger_service import CommunicationRequestLoggerService
from core.communication_system.infrastructure.rockblock_messages_repository import RockBlockMessagesRepository
from core.communication_system.infrastructure.sqlite_communication_system_query_repository import SQLiteCommunicationSystemQueryRepository
from core.iclisten.application.handlers.pam_device_logging_config_event_handler import PAMDeviceLoggingConfigEventHandler
from core.iclisten.application.handlers.pam_device_streaming_config_event_handler import PAMDeviceStreamingConfigEventHandler
from core.iclisten.application.handlers.update_iclisten_device_info_event_handler import UpdateICListenDeviceInfoEventHandler
from core.iclisten.application.ports.iclisten_client import PAMDeviceClient
from core.iclisten.infrastructure.sqlite_iclisten_repository import SQLitePAMSystemRepository
from core.shared.application.notifications_service import NotificationService
from core.shared.domain.db import DBManager
from core.shared.infrastructure.mock_event_bus import InMemoryEventBus
from core.surface_fields.infrastructure.NDFSurfaceFields2DSQueryRepository import \
    NDFSurfaceFields2DSQueryRepository

surface_fields_query_repository = NDFSurfaceFields2DSQueryRepository(
    nc_file_path="../../resources/netCDF_files/rtofs_glo_2ds_f087_prog.nc"
)

# ----------------- Event Bus -----------------
event_bus = InMemoryEventBus()

# ----------------- SQLiteDatabase -----------------
db_manager = DBManager()
session: Session = next(db_manager.get_db())

rockblock_messages_repository = RockBlockMessagesRepository(db=session)

# ----------------- Services -----------------
communication_request_history_repository = SQLCommunicationRequestHistoryRepository(db=session)
communication_request_logger_service = CommunicationRequestLoggerService(
    repository=communication_request_history_repository)

# ----------------- Communicators -----------------
serial_communicator = SerialCommunicator(
    event_bus=event_bus,
    logger=communication_request_logger_service,
    device="COM3"
)
iridium_communicator = IridiumCommunicator(
    logger=communication_request_logger_service
)

communicator_service = CommunicatorService(
    serial_communicator=serial_communicator,
    iridium_communicator=iridium_communicator
)

# ----------------- websockets -----------------
clients: List[WebSocket] = []
notification_service = NotificationService()

# ----------------- ICListen -----------------
pam_system_query_repository = SQLitePAMSystemRepository(db=session)
# iclisten_query_repository = MockPAMSystemRepository()
pam_device_client = PAMDeviceClient(communicator_service=communicator_service)

# ----------------- Communication System -----------------

comm_system_query_repository = SQLiteCommunicationSystemQueryRepository(db=session)
comm_system_request_handler = CommunicationSystemClient(
    communicator_service=communicator_service
)

# ----------------- Event Handlers -----------------
rockblock_message_event_handler = ReceivedRockBlockMessageNotifierEventHandler(
    notification_service=notification_service
)
update_iclisten_device_info_event_handler = UpdateICListenDeviceInfoEventHandler(
    notification_service=notification_service,
    repository=pam_system_query_repository
)

localizer_simple_report_response_event_handler = LocalizerSimpleReportResponseEventHandler(
    notification_service=notification_service,
    repository=comm_system_query_repository
)

drifter_simple_report_response_event_handler = DrifterSimpleReportResponseEventHandler(
    notification_service=notification_service,
    repository=comm_system_query_repository
)

localizer_change_opmode_response_event_handler = LocalizerChangeOpModeResponseEventHandler(
    notification_service=notification_service,
    comm_system_query_repository=comm_system_query_repository,
    request_logger_service=communication_request_logger_service
)

drifter_change_opmode_response_event_handler = DrifterChangeOpModeResponseEventHandler(
    notification_service=notification_service,
    comm_system_query_repository=comm_system_query_repository,
    request_logger_service=communication_request_logger_service
)

drifter_summary_report_response_event_handler = DrifterSummaryReportResponseEventHandler(
    notification_service=notification_service,
    pam_system_repository=pam_system_query_repository,
    communication_system_repository=comm_system_query_repository
)

pam_device_streaming_config_event_handler = PAMDeviceStreamingConfigEventHandler(
    notification_service=notification_service,
    pam_system_repository=pam_system_query_repository,
    request_logger_service=communication_request_logger_service
)

pam_device_logging_config_event_handler = PAMDeviceLoggingConfigEventHandler(
    notification_service=notification_service,
    pam_system_repository=pam_system_query_repository,
    request_logger_service=communication_request_logger_service
)
error_communication_response_event_handler = ErrorCommunicationResponseEventHandler(
    notification_service=notification_service,
    request_logger_service=communication_request_logger_service
)
drifter_reporting_periods_response_event_handler = DrifterReportingPeriodsResponseEventHandler(
    notification_service=notification_service,
    comm_system_query_repository=comm_system_query_repository,
    request_logger_service=communication_request_logger_service
)

# ----------------- Subscriptions -----------------
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
event_bus.subscribe(
    handler=localizer_change_opmode_response_event_handler
)
event_bus.subscribe(
    handler=drifter_change_opmode_response_event_handler
)
event_bus.subscribe(
    handler=drifter_summary_report_response_event_handler
)
event_bus.subscribe(
    handler=pam_device_streaming_config_event_handler
)
event_bus.subscribe(
    handler=pam_device_logging_config_event_handler
)
event_bus.subscribe(
    handler=error_communication_response_event_handler
)
event_bus.subscribe(
    handler=drifter_reporting_periods_response_event_handler
)
