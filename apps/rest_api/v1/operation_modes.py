from fastapi import APIRouter

from apps.rest_api.dependencies import comm_system_request_handler
from core.communication_system.domain.http.change_drifter_op_mode_httprequest import \
    ChangeDrifterOpModeHttpResponse, ChangeDrifterOpModeHttpRequest, ChangeDrifterOpModeParams
from core.communication_system.domain.http.change_localizer_op_mode_httprequest import ChangeLocalizerOpModeHttpRequest, \
    ChangeLocalizerOpModeHttpResponse, ChangeLocalizerOpModeParams
from core.shared.domain.http.httpresponse import HttpResponse

router = APIRouter()


@router.put("/operation-mode/drifter/{mode}", tags=["op-modes-service"])
def change_drifter_op_mode(mode: str) -> HttpResponse[ChangeDrifterOpModeHttpResponse]:
    query = ChangeDrifterOpModeHttpRequest(request_handler=comm_system_request_handler)
    return query.run(
        ChangeDrifterOpModeParams(
            op_mode=int(mode)
        )
    )


@router.put("/operation-mode/localizer/{mode}", tags=["op-modes-service"])
def change_localizer_op_mode(mode: str) -> HttpResponse[ChangeLocalizerOpModeHttpResponse]:
    query = ChangeLocalizerOpModeHttpRequest(request_handler=comm_system_request_handler)
    return query.run(
        ChangeLocalizerOpModeParams(
            op_mode=int(mode)
        )
    )
