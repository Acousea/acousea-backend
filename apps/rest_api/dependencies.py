from core.communication_system.infrastructure.communication_system_request_handler import \
    CommunicationSystemRequestHandler
from core.iclisten.infrastructure.iclisten_request_handler import ICListenRequestHandler
from core.iclisten.infrastructure.recording_stats_repository import RecordingStatsRepository
from core.shared.domain.db import DBManager
from core.shared.infrastructure.communicator.serial_communicator import SerialCommunicator


from core.surface_fields.infrastructure.NDFSurfaceFields2DSQueryRepository import \
    NDFSurfaceFields2DSQueryRepository

surface_fields_query_repository = NDFSurfaceFields2DSQueryRepository(
    nc_file_path="../../resources/netCDF_files/rtofs_glo_2ds_f087_prog.nc"
)

selected_communicator = SerialCommunicator(
    device="COM4",
    baud_rate=9600,
    timeout=3.0
)

# ----------------- ICListen -----------------




# device_query_handler = MockICListenRequestHandler(
#     iclisten_client=iclisten_client
# )

device_query_handler = ICListenRequestHandler(
    communicator=selected_communicator
)

# ----------------- Communication System -----------------


comm_system_request_handler = CommunicationSystemRequestHandler(
    communicator=selected_communicator
)

# ----------------- SQLiteDatabase -----------------
db_manager = DBManager()
session = next(db_manager.get_db())
recording_stats_repository = RecordingStatsRepository(db=session)

