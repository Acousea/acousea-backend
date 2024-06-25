from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel
from core.iclisten.infrastructure.recording_stats_repository import RecordingStatsRepository
from core.shared.domain.http.httprequest import HttpRequest
from core.shared.domain.http.httpresponse import HttpResponse


class GetLatestStatsHttpRequest(HttpRequest[None, RecordingStatsReadModel]):
    def __init__(self, repository: RecordingStatsRepository):
        self.repository = repository

    def execute(self, params: None = None) -> HttpResponse[RecordingStatsReadModel]:
        stats: RecordingStatsReadModel = self.repository.get_latest_stats()
        return HttpResponse.ok(stats)
