from fastapi import APIRouter

from apps.rest_api.dependencies import device_query_handler
from core.iclisten.domain.http.get_device_info_request import GetDeviceInfoHttpRequest, \
    GetDeviceInfoQueryParams

from core.iclisten.domain.device_info_read_model import DeviceInfoReadModel
from core.shared.domain.http.httpresponse import HttpResponse

router = APIRouter()


@router.get("/iclisten/info/{ip}", tags=["iclisten"])
def get_complete_device_info(ip: str) -> HttpResponse[DeviceInfoReadModel]:
    query = GetDeviceInfoHttpRequest(request_handler=device_query_handler)
    return query.run(
        GetDeviceInfoQueryParams(
            ip=ip
        )
    )

