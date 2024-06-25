from fastapi import APIRouter

from apps.rest_api.dependencies import recording_stats_repository
from core.iclisten.domain.http.get_latest_stats_http_request import GetLatestStatsHttpRequest
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel
from core.shared.domain.http.httpresponse import HttpResponse

router = APIRouter()


@router.get("/latest-stats/", tags=["stats-service"])
def read_latest_stats() -> HttpResponse[RecordingStatsReadModel]:
    query = GetLatestStatsHttpRequest(repository=recording_stats_repository)
    return query.run()
