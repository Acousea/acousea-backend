from apps.communication.iclisten_client.communicator.serial_communicator import SerialCommunicator
from data_backend.device.info.infrastructure.mock_device_info_query_repository import MockDeviceInfoQueryRepository
from data_backend.surface_fields.infrastructure.NDFSurfaceFields2DSQueryRepository import \
    NDFSurfaceFields2DSQueryRepository

surface_fields_query_repository = NDFSurfaceFields2DSQueryRepository(
    nc_file_path="../../resources/netCDF_files/rtofs_glo_2ds_f087_prog.nc"
)

device_info_query_repository = MockDeviceInfoQueryRepository()


selected_communicator = SerialCommunicator(
    device="COM3",
    baud_rate=9600,
    timeout=3.0
)


