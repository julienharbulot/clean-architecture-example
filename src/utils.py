import threading
from dataclasses import dataclass
from typing import Any


@dataclass
class CapturedResponse:
    response: Any


class CaptureResponse:
    def __init__(self):
        self._data = threading.local()

    def __call__(self, response: Any) -> CapturedResponse:
        self._data.response = response
        return CapturedResponse(response)

    @property
    def response(self):
        return self._data.response
