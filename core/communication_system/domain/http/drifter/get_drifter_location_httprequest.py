from pydantic import BaseModel

from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetDrifterLocationHttpResponse(BaseModel):
    latitude: float
    longitude: float


class GetDrifterLocationHttpRequest(HttpRequest[None, GetDrifterLocationHttpResponse]):
    def __init__(self, repository: CommunicationSystemQueryRepository):
        self.repository = repository

    def execute(self, params: None = None) -> HttpResponse[GetDrifterLocationHttpResponse]:
        response = self.repository.get_drifter_location()
        if response is None:
            return HttpResponse.fail(message="Drifter location not found (unknown)")
        latitude, longitude = response
        return HttpResponse.ok(GetDrifterLocationHttpResponse(
            latitude=latitude,
            longitude=longitude
        ))
