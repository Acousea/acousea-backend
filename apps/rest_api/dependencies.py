from data_backend.surface_fields.infrastructure.NDFSurfaceFields2DSQueryRepository import \
    NDFSurfaceFields2DSQueryRepository

surface_fields_query_repository = NDFSurfaceFields2DSQueryRepository(
    nc_file_path="../../resources/netCDF_files/rtofs_glo_2ds_f087_prog.nc"
)

