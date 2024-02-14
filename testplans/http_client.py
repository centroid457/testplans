import time
from typing import *
import requests
from PyQt5.QtCore import QThread
from enum import Enum, auto
from collections import deque

from object_info import ObjectInfo


# =====================================================================================================================
Type_Response = Union[None, requests.Response, requests.ConnectTimeout]
Type_RequestBody = Union[str, dict]


# =====================================================================================================================
class UrlCreator:
    # SETTINGS -------------------------------------
    PROTOCOL: str = "http"
    HOST: str = "localhost"
    PORT: int = 80
    ROUTE: str = "stop123"

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
        return url


class RequestItem:
    # SETTINGS -------------------------------------


    # AUX ------------------------------------------
    BODY: Type_RequestBody
    # REQUEST: Optional[requests.Request] = None
    RESPONSE: Optional[requests.Response] = None
    EXX_TIMEOUT: Union[None, requests.ConnectTimeout, Exception] = None
    attempt: int
    index: int = 0

    def __init__(self, body: Type_RequestBody):
        self.__class__.index += 1
        self.BODY = body
        self.attempt = 0
        self.index = int(self.__class__.index)

    def check_success(self) -> bool:
        result = self.RESPONSE is not None and self.RESPONSE.ok
        return result

    def attempt_next(self) -> None:
        self.attempt += 1

    def __str__(self) -> str:
        return f"[{self.index=}/{self.attempt=}]{self.EXX_TIMEOUT=}/{self.RESPONSE=}"

    def __repr__(self) -> str:
        return str(self)


# =====================================================================================================================
class HttpClient(UrlCreator, QThread):
    # TODO: add timestamp
    # TODO: save send data

    # SETTINGS -------------------------------------
    TIMEOUT_SEND: float = 1

    RETRY_LIMIT: int = 2
    RETRY_TIMEOUT: float = 0.5

    # AUX ------------------------------------------
    __stack: deque
    request_last: Optional[RequestItem] = None

    def __init__(self):
        super().__init__()
        self.__class__.__stack = deque()

    @classmethod
    @property
    def STACK(cls) -> deque:
        return cls.__stack

    # ------------------------------------------------------------------------------------------------
    def start(self, *args):
        if not self.isRunning():
            super().start(*args)

    # ------------------------------------------------------------------------------------------------
    def run(self):
        retry_count = 0
        url = self.URL_create()
        while len(self.STACK):
            # NEXT -----------------------------------------
            if self.request_last is None or self.request_last.check_success():
                retry_count = 0
                self.request_last = self.STACK[0]

            # WORK -----------------------------------------
            self.request_last.attempt_next()
            with requests.Session() as session:
                try:
                    response = session.post(url=url, data=self.request_last.BODY, timeout=self.TIMEOUT_SEND)
                    self.request_last.RESPONSE = response
                except Exception as exx:
                    self.request_last.EXX_TIMEOUT = exx

            if self.request_last.check_success():
                retry_count = 0
                self.STACK.popleft()
                continue

            print()
            print(f"{self.request_last=}")
            print(f"{self.STACK=}")

            if retry_count >= self.RETRY_LIMIT:
                break
            else:
                retry_count += 1
                time.sleep(self.RETRY_TIMEOUT)

    def post(self, body: Optional[dict] = None):
        # TODO: add locker???
        body = body or {}
        item = RequestItem(body)
        self.STACK.append(item)
        self.start()


# =====================================================================================================================
