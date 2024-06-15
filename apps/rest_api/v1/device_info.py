from fastapi import APIRouter

from apps.rest_api.dependencies import device_info_query_repository
from data_backend.device.info.application.queries.get_device_info_query import GetDeviceInfoHttpRequest, \
    GetDeviceInfoQueryParams
from data_backend.device.info.domain.device_info_read_model import DeviceInfoReadModel
from data_backend.shared.domain.httpresponse import HttpResponse

router = APIRouter()


@router.get("/device-info/{ip}", tags=["device-info"])
def get_complete_device_info(ip: str) -> HttpResponse[DeviceInfoReadModel]:
    query = GetDeviceInfoHttpRequest(query_repository=device_info_query_repository)
    return query.run(
        GetDeviceInfoQueryParams(
            ip=ip
        )
    )
