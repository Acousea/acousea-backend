from pydantic import BaseModel

from core.communication_system.application.ports.communication_system_query_repository import CommunicationSystemQueryRepository
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetLocalizerLocationHttpResponse(BaseModel):
    latitude: float
    longitude: float


class GetLocalizerLocationHttpRequest(HttpRequest[None, GetLocalizerLocationHttpResponse]):
    def __init__(self, repository: CommunicationSystemQueryRepository):
        self.repository = repository

    def execute(self, params: None = None) -> HttpResponse[GetLocalizerLocationHttpResponse]:
        response = self.repository.get_localizer_location()
        if response is None:
            return HttpResponse.fail(message="Localizer location not found (unknown)")
        latitude, longitude = response
        return HttpResponse.ok(GetLocalizerLocationHttpResponse(
            latitude=latitude,
            longitude=longitude
        ))
