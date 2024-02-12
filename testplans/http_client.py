from typing import *
import requests
from PyQt5.QtCore import QThread
from enum import Enum, auto

from object_info import ObjectInfo


class TypeRequest(Enum):
    GET = auto()
    POST = auto()
    # HEAD = auto()
    # DELETE = auto()
    # PATCH = auto()
    # OPTIONS = auto()


class UrlCreator:
    # SETTINGS -------------------------------------
    PROTOCOL: str = "http"
    HOST: str = "localhost"
    PORT: int = 80
    ROUTE: str = ""
    TYPE_REQUEST: TypeRequest = TypeRequest.POST

    def URL_create(
            self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            route: Optional[str] = None,
    ) -> str:
        if host is None:
            host = self.HOST
        if port is None:
            port = self.PORT
        if route is None:
            route = self.ROUTE

        url = f"{self.PROTOCOL}://{host}:{port}/{route}"
        print(f"{url=}")
        return url


class HttpClient(UrlCreator, QThread):
    """
    THREADS!

    NOTE:
    1. typical usage
        class Cls:
            POST = HttpClient
        Cls().POST(body={})
    # 2. sometimes it will not work! so use second way (and maybe it is preferred)
    #     class Cls:
    #         POST = HttpClient()
    #     Cls().POST.post(body={})
    """
    # SETTINGS -------------------------------------
    BODY: Optional[Any] = None
    TIMEOUT_SEND: float = 1

    # AUX ------------------------------------------
    response: requests.Response = None
    # history: List[requests.Response] = []

    def __init__(self, body: Optional[dict] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if body is not None:
            self.BODY = body
            self.start()

    def run(self):
        url = self.URL_create()
        with requests.Session() as session:
            if self.TYPE_REQUEST == TypeRequest.POST:
                response = session.post(url=url, data=self.BODY, timeout=self.TIMEOUT_SEND)
            elif self.TYPE_REQUEST == TypeRequest.GET:
                response = session.get(url=url, timeout=self.TIMEOUT_SEND)

            self.response_apply(response)

    def response_apply(self, response: requests.Response) -> None:
        self.response = response
        # self.history.append(response)

    # def post(self, body: Optional[dict] = None) -> None:
    #     # if body is not None:
    #     #     self.BODY = body
    #
    #     self.TYPE_REQUEST = TypeRequest.POST
    #     self.start()
try
# class HttpClient2(HttpClient):
#     ROUTE = "start"
#
#
# if __name__ == "__main__":
#     # Tp_obj = TestPlan_example1()
#
#     HttpClient2({}).wait()
