import asyncio
from msgflow import Channel, Message, PipelineChannelMixin
from typing import Any
from aiohttp import web


class WebapiChannel(Channel, PipelineChannelMixin):
    def __init__(self, host, port, routes):
        self._host = host
        self._port = port
        self._routes = routes

    async def flow(self, queue: asyncio.Queue) -> None:
        async def handler(request):
            msg = Message(req=request, res=None, service=self)
            await queue.put(msg)
            print(f"Queue updated: size={queue.qsize()}, object={queue}")
            await msg.wait_response()
            return msg.res

        # https://docs.aiohttp.org/en/stable/web_advanced.html#application-runners
        app = web.Application()
        for method, path in self._routes:
            app.add_routes([getattr(web, method)(path, handler)])

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, self._host, self._port)
        await site.start()
        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            print("Clean up")
            # wait for finish signal
            await runner.cleanup()

    async def post(self, obj: Any) -> None:
        raise NotImplementedError()


class WebapiMessage(Message):
    def __init__(self, channel, req, res):
        """"""
        self._req = req
        self._res = res
        self._channel = channel
        self._event = asyncio.Event()

    @property
    def channel(self) -> Channel:
        return self._channel

    async def respond(self, obj: str) -> None:
        self._res = obj
        self._event.set()

    @property
    def req(self):
        return self._req

    @property
    def res(self):
        return self._res

    async def wait_response(self):
        return self._event.wait()
