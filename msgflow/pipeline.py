import asyncio
from pydantic import BaseModel
from msgflow import Channel
from typing import Any, Optional
import re
import inspect


class PipelineChannelMixin:
    @property
    def name(self) -> str:
        return self._pipeline_provider_name

    def set_name(self, name):
        self._pipeline_provider_name = name


class Pipeline:
    def __init__(self, app):
        # List up all methods which has "config" attr set by `handler` decorator
        handlers = []
        for method_name in dir(app):
            method = getattr(app, method_name)
            if hasattr(method, "config"):
                handlers.append(method)

        print(handlers)
        self._handlers = handlers

        # Create a list including input channels
        input_channels = []
        if isinstance(app.input_channel, dict):
            # Sort may be needed
            for svc_name, svc in app.input_channel.items():
                svc.set_name(svc_name)
                input_channels.append(svc)
        elif isinstance(app.input_channel, list):
            input_channels = app.input_channel
        else:
            input_channels = [app.input_channel]

        self._input_channels = input_channels

    async def _handle(self, queue):
        while True:
            msg = await queue.get()
            for handler in self._handlers:
                # Logging
                print(f"handler: {handler.__name__}, config: {handler.config}")

                if not handler.config.enabled:
                    continue
                if (handler.config.channel_name is not None) and (msg.channel.name != handler.config.channel_name):
                    continue
                if (handler.config.cond is not None) and (not handler.config.cond(msg)):
                    continue

                match = None
                if handler.config.pattern is not None:
                    match = re.match(handler.config.pattern, handler.config.pattern_attr(msg))
                    if match is None:
                        continue

                # Get handlers argument names
                handler_arg_names = inspect.getfullargspec(handler).args[1:]  # use [1:] to remove first "self"

                # Set up argument to pass to handler
                possible_arg_map = {"msg": msg, "match": match}
                args = dict()
                for arg in handler_arg_names:
                    if arg in possible_arg_map:
                        args[arg] = possible_arg_map[arg]
                    else:
                        raise Exception(f"{arg} should be one of {set(possible_arg_map.keys())}")
                await handler(**args)

                # If one of handlers matches, other handlers will be ignored
                #break

    async def run(self):
        queue = asyncio.Queue()

        # Create tasks and **schedule to run soon concurrently**
        service_tasks = []
        for service in self._input_channels:
            svc_task = asyncio.create_task(service.flow(queue=queue))
            #svc_task.set_name(f"{svc_task.get_name()}-{service.name}")
            service_tasks.append(svc_task)
        handler_task = asyncio.create_task(self._handle(queue=queue))

        # Check one of service tasks completes
        # Use wait to check one of service/task is completed or raise error
        done, pending = await asyncio.wait(
            service_tasks + [handler_task],
            return_when=asyncio.FIRST_COMPLETED
        )


def _default_pattern_attr(msg):
    raise NotImplementedError("Specify which attribute to use for pattern match")


class HandlerConfig(BaseModel):
    enabled: bool
    channel_name: Optional[str]
    cond: Optional[Any]
    pattern: Optional[str]
    pattern_attr: Any = _default_pattern_attr


def handler(
    _func=None, *,
    channel=None,
    cond=None,
    pattern=None,
    pattern_attr=_default_pattern_attr,
):
    """Tag function as a handler of service
    """

    def decorator(func):
        # Set "config" attribute
        func.config = HandlerConfig(
            enabled=True,
            channel_name=channel,
            cond=cond,
            pattern=pattern,
            pattern_attr=pattern_attr,
        )
        return func

    if _func is None:
        # when handler is called with arguments,,
        # _func is set to None
        return decorator
    else:
        # when handler is called without arguments,
        # _func is set to the function to be decorated
        return decorator(_func)
