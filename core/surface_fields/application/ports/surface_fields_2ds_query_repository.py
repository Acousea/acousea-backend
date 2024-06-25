from abc import ABC, abstractmethod

import netCDF4
import pkg_resources

from core.surface_fields.domain.single_lat_lon_uv_read_model import SingleLatLonUVReadModel


class SurfaceFields2DSQueryRepository(ABC):

    def __init__(self, resource_file_name: str):
        self.dataset = netCDF4.Dataset(resource_file_name, "r")

    @abstractmethod
    def get_all(self) -> list[list[SingleLatLonUVReadModel]]:
        pass

    @abstractmethod
    def get_by_lat_lon(self, target_latitude: str, target_longitude: str) -> SingleLatLonUVReadModel:
        pass
