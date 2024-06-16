import os

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.staticfiles import StaticFiles
from apps.rest_api.v1.surface_fields import router as surface_fields_router
from apps.rest_api.v1.device_info import router as device_info_router
from apps.rest_api.v1.ping import router as ping_router


from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5734",
    "*"
]

description = """
The **RTOFS Fields** API allows you to get RTOFS fields data.
It provides various endpoints for obtaining different fields data in multiple formats.
It also allows you to retrieve surface fields and their details.
"""

tags_metadata = [
    {
        "name": "surface_fields",
        "description": "Operations related to surface fields. This subdomain enables you to retrieve surface fields and their details.",
    },
    {
        "name": "iclisten",
        "description": "Operations related to iclisten information. This subdomain enables you to retrieve iclisten information and their details.",
    },
    {
        "name": "ping-service",
        "description": "Operations related to ping service. This subdomain enables you to ping the iclisten and get the response.",
    },

]

app = FastAPI(
    title="RTOFS REST API",
    description=description,
    summary="This is RTOFS rest api for integrations",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(surface_fields_router, prefix="/api/v1")
app.include_router(device_info_router, prefix="/api/v1")
app.include_router(ping_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
