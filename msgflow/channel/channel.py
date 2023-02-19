import asyncio
from typing import Any


class Channel:
    async def flow(self, queue: asyncio.Queue) -> None:
        """flow metiod is supposed to be called by asyncio.create_task.
        Then it puts messaegs in a queue given as an argument.
        """
        raise NotImplementedError()

    async def post(self, obj: Any) -> None:
        raise NotImplementedError()


class Message:
    @property
    def channel(self) -> Channel:
        raise NotImplementedError()

    async def respond(self, obj: Any) -> None:
        raise NotImplementedError
