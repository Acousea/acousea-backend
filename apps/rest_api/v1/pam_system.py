from fastapi import APIRouter

from apps.rest_api.dependencies import pam_system_query_repository, pam_device_client
from core.iclisten.domain.http.get_device_info_request import GetDeviceInfoHttpRequest
from core.iclisten.domain.http.get_device_streaming_config_request import GetPAMDeviceStreamingConfigHttpRequest, \
    CommunicationResultHttpResponse
from core.iclisten.domain.http.get_latest_stats_http_request import GetLatestStatsHttpRequest
from core.iclisten.domain.http.retrieve_device_logging_config_request import RetrieveDeviceLoggingConfigHttpRequest
from core.iclisten.domain.http.retrieve_device_streaming_config_request import RetrieveDeviceStreamingConfigHttpRequest
from core.iclisten.domain.http.set_device_streaming_config_request import SetDeviceStreamingConfigHttpRequest, \
    SetPAMDeviceStreamingConfigRequestParams
from core.iclisten.domain.http.update_device_info_request import UpdateICListenDeviceInfoHttpRequest, UpdateICListenDeviceInfoQueryParams
from core.iclisten.domain.pam_system_logging_config_read_model import PAMDeviceLoggingConfigReadModel
from core.iclisten.domain.pam_system_status_info_read_model import PAMDeviceStatusReadModel
from core.iclisten.domain.pam_system_streaming_config_read_model import PAMDeviceStreamingConfigReadModel
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel
from core.shared.domain.http.httpresponse import HttpResponse

router = APIRouter()


@router.get("/pam-system/latest-stats", tags=["pam-system"])
def read_latest_stats() -> HttpResponse[RecordingStatsReadModel]:
    query = GetLatestStatsHttpRequest(repository=pam_system_query_repository)
    return query.run()


@router.get("/pam-system/info", tags=["pam-system"])
def get_complete_device_info() -> HttpResponse[PAMDeviceStatusReadModel]:
    query = GetDeviceInfoHttpRequest(pam_system_repository=pam_system_query_repository)
    return query.run()


@router.get("/pam-system/logging-configuration", tags=["pam-system"])
def retrieve_device_logging_config() -> HttpResponse[PAMDeviceLoggingConfigReadModel]:
    query = RetrieveDeviceLoggingConfigHttpRequest(pam_system_repository=pam_system_query_repository)
    return query.run()


@router.get("/pam-system/streaming-configuration", tags=["pam-system"])
def retrieve_complete_device_info() -> HttpResponse[PAMDeviceStreamingConfigReadModel]:
    query = RetrieveDeviceStreamingConfigHttpRequest(pam_system_repository=pam_system_query_repository)
    return query.run()


@router.get("/pam-system/streaming-configuration/update", tags=["pam-system"])
def get_complete_device_info() -> HttpResponse[CommunicationResultHttpResponse]:
    query = GetPAMDeviceStreamingConfigHttpRequest(pam_device_client=pam_device_client)
    return query.run()


@router.post("/pam-system/streaming-configuration/set", tags=["pam-system"])
def set_device_streaming_config(params: SetPAMDeviceStreamingConfigRequestParams) -> HttpResponse[CommunicationResultHttpResponse]:
    query = SetDeviceStreamingConfigHttpRequest(pam_device_client=pam_device_client)
    return query.run(params)


@router.get("/pam-system/info/update/{ip}", tags=["pam-system"])
def get_complete_device_info(ip: str) -> HttpResponse[CommunicationResultHttpResponse]:
    query = UpdateICListenDeviceInfoHttpRequest(client=pam_device_client)
    return query.run(
        UpdateICListenDeviceInfoQueryParams(
            ip=ip
        )
    )
