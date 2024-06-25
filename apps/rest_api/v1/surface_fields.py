from fastapi import APIRouter

from apps.rest_api.dependencies import surface_fields_query_repository
from core.shared.domain.http.httpresponse import HttpResponse

from core.surface_fields.application.queries.get_surface_fields_u_v_for_given_lat_long_query import \
    GetSurfaceFieldsUVForGivenLatLonHttpRequest, GetSurfaceFieldsUVForGivenLatLonQueryParams
from core.surface_fields.domain.single_lat_lon_uv_read_model import SingleLatLonUVReadModel


router = APIRouter()


@router.get("/surface-fields/latest/{latitude}/{longitude}/", tags=["surface_fields"])
def get_surface_fields_u_v_for_given_lat_lon(latitude: str, longitude: str) -> HttpResponse[SingleLatLonUVReadModel]:
    query = GetSurfaceFieldsUVForGivenLatLonHttpRequest(query_repository=surface_fields_query_repository)
    return query.run(
        GetSurfaceFieldsUVForGivenLatLonQueryParams(
            latitude=latitude,
            longitude=longitude
        )
    )
