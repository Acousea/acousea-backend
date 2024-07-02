from core.iclisten.application.ports.iclisten_repository import ICListenRepository
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel

from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetLatestStatsHttpRequest(HttpRequest[None, RecordingStatsReadModel]):
    def __init__(self, repository: ICListenRepository):
        self.repository = repository

    def execute(self, params: None = None) -> HttpResponse[RecordingStatsReadModel]:
        stats: RecordingStatsReadModel = self.repository.get_latest_stats()
        return HttpResponse.ok(stats)
