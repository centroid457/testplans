import pathlib
from typing import *

from server_templates import ServerAiohttpBase, decorator__log_request_response, web


# =====================================================================================================================
class TpApi(ServerAiohttpBase):
    async def response_get__(self, request) -> web.Response:
        # --------------------------
        progress = 0
        if self.data and self.data.progress is not None:
            progress = self.data.progress
        # --------------------------
        html_block = f"[PROGRESS = {progress}%]<br /><br />" + self.html_block__api_index()

        # HTML --------------------------------------------------
        page_name = "API_INDEX"
        html = self.html_create(name=page_name, data=html_block, redirect_time=2, request=request)
        return web.Response(text=html, content_type='text/html')

    @decorator__log_request_response
    async def response_get__start(self, request) -> web.Response:
        self.data.signal__tp_start.emit()

        # HTML --------------------------------------------------
        page_name = "START"
        html = self.html_create(name=page_name, redirect_time=1, request=request)
        return web.Response(text=html, content_type='text/html')

    @decorator__log_request_response
    async def response_get__stop(self, request) -> web.Response:
        self.data.signal__tp_stop.emit()

        # HTML --------------------------------------------------
        page_name = "STOP"
        html = self.html_create(name=page_name, redirect_time=1, request=request)
        return web.Response(text=html, content_type='text/html')

    @decorator__log_request_response
    async def response_post__start(self, request) -> web.Response:
        # return self.response_get__start(request)  # this is will not work!
        await self.response_get__start(request)
        response = web.json_response(data={})
        return response

    @decorator__log_request_response
    async def response_post__stop(self, request) -> web.Response:
        await self.response_get__stop(request)
        response = web.json_response(data={})
        return response

    # ---------------------------------------------------------
    @decorator__log_request_response
    async def response_get__info_json(self, request) -> web.Response:
        body: dict = self.data.info_get()
        response = web.json_response(data=body)
        return response

    @decorator__log_request_response
    async def response_get__info_html(self, request) -> web.Response:
        """
        this is only for pretty view
        """
        # HTML --------------------------------------------------
        page_name = "INFO_HTML"
        html = self.html_create(name=page_name, data=self.data.info_get(), request=request)
        return web.Response(text=html, content_type='text/html')

    # ---------------------------------------------------------
    @decorator__log_request_response
    async def response_get__results_json(self, request) -> web.Response:
        body: dict = self.data.results_get()
        response = web.json_response(data=body)
        return response

    @decorator__log_request_response
    async def response_get__results_html(self, request) -> web.Response:
        """
        this is only for pretty view
        """
        # HTML --------------------------------------------------
        page_name = "INFO_HTML"
        html = self.html_create(name=page_name, data=self.data.results_get(), request=request)
        return web.Response(text=html, content_type='text/html')


# =====================================================================================================================
