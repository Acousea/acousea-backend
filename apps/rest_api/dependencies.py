from data_backend.drifter.domain.drifter_client import DrifterClient
from data_backend.drifter.infrastructure.serial_drifter_request_handler import SerialDrifterRequestHandler
from data_backend.iclisten.domain.ICListenClient import ICListenClient
from apps.communication.communicator.serial_communicator import SerialCommunicator
from data_backend.iclisten.infrastructure.serial_iclisten_request_handler import SerialICListenRequestHandler

from data_backend.surface_fields.infrastructure.NDFSurfaceFields2DSQueryRepository import \
    NDFSurfaceFields2DSQueryRepository

surface_fields_query_repository = NDFSurfaceFields2DSQueryRepository(
    nc_file_path="../../resources/netCDF_files/rtofs_glo_2ds_f087_prog.nc"
)

selected_communicator = SerialCommunicator(
    device="COM3",
    baud_rate=9600,
    timeout=3.0
)

iclisten_client = ICListenClient(
    communicator=selected_communicator
)

# device_query_handler = MockICListenRequestHandler(
#     iclisten_client=iclisten_client
# )

device_query_handler = SerialICListenRequestHandler(
    iclisten_client=iclisten_client
)

drifter_client = DrifterClient(
    communicator=selected_communicator
)

drifter_query_handler = SerialDrifterRequestHandler(
    drifter_client=drifter_client
)







