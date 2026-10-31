from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from sentry.shared_integrations.response.base import BaseApiResponse


# justification: API response payloads are decoded JSON of mixed types.
class MappingApiResponse(dict[str, Any], BaseApiResponse):
    def __init__(self, data: Mapping[str, Any], *args: Any, **kwargs: Any) -> None:
        dict.__init__(self, data)
        BaseApiResponse.__init__(self, *args, **kwargs)

    @property
    def json(self) -> Any:
        return self
