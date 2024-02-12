import time
from typing import *
import requests
from PyQt5.QtCore import QThread
from enum import Enum, auto

from object_info import ObjectInfo

Type_Response = Union[requests.Response, requests.ConnectTimeout]


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
    TIMEOUT_SEND: float = 1

    RETRY_LIMIT: int = 0
    RETRY_TIMEOUT: float = 0.1

    # AUX ------------------------------------------
    que_posted: int = 0
    que_len: int = 0
    que: Dict[int, Dict[str, Union[dict, Type_Response]]] = {}

    in_progress: bool = None

    def run(self):
        if self.in_progress:
            print(1111111)
            return

        self.in_progress = True
        retry_count = 0

        url = self.URL_create()
        while self.que_len != self.que_posted:
            print(f"while_block=[{self.que_len=}/{self.que_posted=}]{self.que=}")
            response_dict = self.que.get(self.que_posted + 1)
            if response_dict is None:
                print(f"no {response_dict=}")
                break

            body = response_dict.get("body")
            if body is None:
                print(f"no {body=}")
                break

            with requests.Session() as session:
                response = None
                try:
                    response = session.post(url=url, data=body, timeout=self.TIMEOUT_SEND)
                except Exception as exx:
                    retry_count += 1
                    print(f"{exx!r}")
                    response = exx

                    if retry_count > self.RETRY_LIMIT:
                        pass
                    else:
                        time.sleep(self.RETRY_TIMEOUT)
                        continue

                if response is not None:
                    retry_count = 0
                    self._response_apply(response)

        # FINISH ------------------------------------------
        self.in_progress = False
        print(f"start_FINISHED=[{self.que_len}]{self.que=}")

    def _response_apply(self, response: Type_Response) -> None:
        print()
        print()
        print()
        print(f"{response=}")
        self.que_posted += 1
        print(f"{self.que_posted=}")
        print(f"{self.que=}")
        print(f"{self.que[self.que_posted]=}")
        self.que[self.que_posted].update({"response": response})

    def post(self, body: Optional[dict] = None):
        # TODO: add locker
        body = body or {}
        self.que_len += 1
        print(f"[{self.que_len}]{body=}")
        self.que.update({self.que_len: {"body": body}})
        print(11)
        self.start()


# class HttpClient2(HttpClient):
#     ROUTE = "start"
#
#
# if __name__ == "__main__":
#     # Tp_obj = TestPlan_example1()
#
#     HttpClient2({}).wait()
