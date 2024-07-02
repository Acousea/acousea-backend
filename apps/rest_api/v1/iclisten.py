from fastapi import APIRouter

from apps.rest_api.dependencies import iclisten_query_repository, iclisten_client
from core.iclisten.domain.iclisten_device_info_read_model import ICListenDeviceInfoReadModel
from core.iclisten.domain.http.get_device_info_request import GetDeviceInfoHttpRequest, \
    GetDeviceInfoQueryParams
from core.iclisten.domain.http.get_latest_stats_http_request import GetLatestStatsHttpRequest
from core.iclisten.domain.http.update_device_info_request import UpdateICListenDeviceInfoHttpRequest, UpdateICListenDeviceInfoQueryParams, \
    UpdateICListenDeviceInfoRequestResult
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel
from core.shared.domain.http.httpresponse import HttpResponse

router = APIRouter()


@router.get("/iclisten/latest-stats/", tags=["stats-service"])
def read_latest_stats() -> HttpResponse[RecordingStatsReadModel]:
    query = GetLatestStatsHttpRequest(repository=iclisten_query_repository)
    return query.run()


@router.get("/iclisten/info/{ip}", tags=["iclisten"])
def get_complete_device_info(ip: str) -> HttpResponse[ICListenDeviceInfoReadModel]:
    query = GetDeviceInfoHttpRequest(repository=iclisten_query_repository)
    return query.run(
        GetDeviceInfoQueryParams(
            ip=ip
        )
    )


@router.get("/iclisten/info/update/{ip}", tags=["iclisten"])
def get_complete_device_info(ip: str) -> HttpResponse[UpdateICListenDeviceInfoRequestResult]:
    query = UpdateICListenDeviceInfoHttpRequest(client=iclisten_client)
    return query.run(
        UpdateICListenDeviceInfoQueryParams(
            ip=ip
        )
    )
