from fastapi import APIRouter

from apps.rest_api.dependencies import iclisten_query_repository, iclisten_client
from core.iclisten.domain.http.get_device_info_request import GetDeviceInfoHttpRequest
from core.iclisten.domain.http.get_device_logging_config_request import GetDeviceLoggingConfigHttpRequest
from core.iclisten.domain.http.get_device_streaming_config_request import GetDeviceStreamingConfigHttpRequest
from core.iclisten.domain.http.get_latest_stats_http_request import GetLatestStatsHttpRequest
from core.iclisten.domain.http.update_device_info_request import UpdateICListenDeviceInfoHttpRequest, UpdateICListenDeviceInfoQueryParams, \
    UpdateICListenDeviceInfoRequestResult
from core.iclisten.domain.pam_system_logging_config_read_model import PAMDeviceLoggingConfigReadModel
from core.iclisten.domain.pam_system_status_info_read_model import PAMDeviceStatusReadModel
from core.iclisten.domain.pam_system_streaming_config_read_model import PAMDeviceStreamingConfigReadModel
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel
from core.shared.domain.http.httpresponse import HttpResponse

router = APIRouter()


@router.get("/pam-system/latest-stats/", tags=["pam-system"])
def read_latest_stats() -> HttpResponse[RecordingStatsReadModel]:
    query = GetLatestStatsHttpRequest(repository=iclisten_query_repository)
    return query.run()


@router.get("/pam-system/info", tags=["pam-system"])
def get_complete_device_info() -> HttpResponse[PAMDeviceStatusReadModel]:
    query = GetDeviceInfoHttpRequest(pam_system_repository=iclisten_query_repository)
    return query.run()


@router.get("/pam-system/logging-configuration", tags=["pam-system"])
def get_complete_device_info() -> HttpResponse[PAMDeviceLoggingConfigReadModel]:
    query = GetDeviceLoggingConfigHttpRequest(pam_system_repository=iclisten_query_repository)
    return query.run()


@router.get("/pam-system/streaming-configuration", tags=["pam-system"])
def get_complete_device_info() -> HttpResponse[PAMDeviceStreamingConfigReadModel]:
    query = GetDeviceStreamingConfigHttpRequest(pam_system_repository=iclisten_query_repository)
    return query.run()


@router.get("/pam-system/info/update/{ip}", tags=["pam-system"])
def get_complete_device_info(ip: str) -> HttpResponse[UpdateICListenDeviceInfoRequestResult]:
    query = UpdateICListenDeviceInfoHttpRequest(client=iclisten_client)
    return query.run(
        UpdateICListenDeviceInfoQueryParams(
            ip=ip
        )
    )
