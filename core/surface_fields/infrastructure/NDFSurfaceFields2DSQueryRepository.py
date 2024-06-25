import numpy as np

from core.surface_fields.application.ports.surface_fields_2ds_query_repository import \
    SurfaceFields2DSQueryRepository
from core.surface_fields.domain.single_lat_lon_uv_read_model import SingleLatLonUVReadModel


class NDFSurfaceFields2DSQueryRepository(SurfaceFields2DSQueryRepository):

    def __init__(self, nc_file_path: str):
        super().__init__("resources/netCDF_files/rtofs_glo_2ds_f087_prog.nc")
        # Extrae las variables necesarias
        self.latitudes = self.dataset.variables['Latitude'][:]
        self.longitudes = self.dataset.variables['Longitude'][:]
        self.u_currents = self.dataset.variables['u_velocity'][0, 0, :, :]  # Primer paso temporal, primera capa
        self.v_currents = self.dataset.variables['v_velocity'][0, 0, :, :]  # Primer paso temporal, primera capa

        # Recalculate longitudes to be in the range of -180 to 180 (do modulo 360)
        self.longitudes = np.mod(self.longitudes + 180, 360) - 180

    def get_all(self) -> list[list[SingleLatLonUVReadModel]]:
        pass

    def get_by_lat_lon(self, target_latitude: str, target_longitude: str) -> SingleLatLonUVReadModel:
        print("Target Latitude: ", target_latitude)
        print("Target Longitude: ", target_longitude)

        target_longitude = float(target_longitude)
        target_latitude = float(target_latitude)

        # Encontrar el índice más cercano a la latitud y longitud objetivo
        lat_diff = np.abs(self.latitudes - target_latitude)
        lon_diff = np.abs(self.longitudes - target_longitude)
        total_diff = lat_diff + lon_diff

        min_diff_index = np.unravel_index(np.nanargmin(total_diff, axis=None), total_diff.shape)
        nearest_lat = self.latitudes[min_diff_index]
        nearest_lon = self.longitudes[min_diff_index]
        u_current = self.u_currents[min_diff_index]
        v_current = self.v_currents[min_diff_index]

        # Asegúrate de que los valores no sean NaN
        if np.isnan(nearest_lat) or np.isnan(nearest_lon):
            raise ValueError("The nearest latitude or longitude was not found or is NaN")

        # Limit to 2 decimal places
        return SingleLatLonUVReadModel(
            latitude=str(nearest_lat),
            longitude=str(nearest_lon),
            u_velocity=str(u_current),
            v_velocity=str(v_current)
        )
