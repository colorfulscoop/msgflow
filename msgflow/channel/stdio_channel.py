import asyncio
from msgflow import Channel, Message, PipelineChannelMixin
import sys
import aioconsole


class StdioChannel(Channel, PipelineChannelMixin):
    def __init__(self, user_name: str, in_fd=sys.stdin, out_fd=sys.stdout):
        self._user_name = user_name
        self._in_fd = in_fd
        self._out_fd = out_fd

    async def flow(self, queue: asyncio.Queue) -> None:
        while True:
            try:
                text = await aioconsole.ainput(f"{self._user_name}> ")
            except (KeyboardInterrupt, EOFError):
                print("Bye!", file=self._out_fd)
                break

            msg = StdioMessage(channel=self, req=text)
            await queue.put(msg)
            await msg.wait_response()

    async def post(self, obj: str) -> None:
        print(obj, file=self._out_fd)

    @property
    def out_fd(self):
        return self._out_fd


class StdioMessage(Message):
    def __init__(self, channel, req=None, res=None):
        self._req = req
        self._res = res
        self._channel = channel
        self._event = asyncio.Event()

    @property
    def channel(self) -> Channel:
        return self._channel

    async def respond(self, obj: str) -> None:
        print(f">>> {obj}", file=self._channel.out_fd)
        self._event.set()

    @property
    def req(self):
        return self._req

    @property
    def res(self):
        return self._res

    async def wait_response(self):
        await self._event.wait()
