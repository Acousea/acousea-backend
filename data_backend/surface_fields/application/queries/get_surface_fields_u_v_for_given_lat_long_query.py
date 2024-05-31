from pydantic import BaseModel

from data_backend.shared.application.query import Query
from data_backend.shared.domain.response import Response
from data_backend.surface_fields.application.ports.surface_fields_2ds_query_repository import SurfaceFields2DSQueryRepository
from data_backend.surface_fields.domain.single_lat_lon_uv_read_model import SingleLatLonUVReadModel


class GetSurfaceFieldsUVForGivenLatLonQueryParams(BaseModel):
    latitude: str
    longitude: str


class GetSurfaceFieldsUVForGivenLatLonQuery(Query[GetSurfaceFieldsUVForGivenLatLonQueryParams, SingleLatLonUVReadModel]):
    def __init__(self, query_repository: SurfaceFields2DSQueryRepository):
        self.query_repository = query_repository

    def execute(self, params: GetSurfaceFieldsUVForGivenLatLonQueryParams | None = None) -> Response[list[SingleLatLonUVReadModel]]:
        if params is None:
            return Response.fail(message="You need to pass a latitude and a longitude")
        return Response.ok(self.query_repository.get_by_lat_lon(
            target_latitude=params.latitude,
            target_longitude=params.longitude
        ))
