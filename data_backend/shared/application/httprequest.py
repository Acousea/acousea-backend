import json
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import ValidationError

from data_backend.shared.domain.httpresponse import HttpResponse

QueryResult = TypeVar("QueryResult")
QueryParams = TypeVar("QueryParams")


class HttpRequest(ABC, Generic[QueryParams, QueryResult]):
    @abstractmethod
    def execute(self, params: QueryParams | None = None) -> HttpResponse[QueryResult]:
        pass

    def run(self, params: QueryParams | None = None) -> HttpResponse[QueryResult]:
        try:
            return self.execute(params)
        except ValidationError as e:
            field: list[str] = json.loads(e.json())[0]["loc"]
            return HttpResponse.field_fail(message='{} must be valid'.format(", ".join(field)), field=field)
        except ValueError as e:
            return HttpResponse.fail(message=str(e))
        except Exception as e:
            return HttpResponse.fail(code=-1, message=str(e))
