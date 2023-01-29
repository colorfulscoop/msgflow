import asyncio
import sys


class PipelineMixin:
    @property
    def name(self) -> str:
        return self._pipeline_provider_name

    def set_name(self, name):
        self._pipeline_provider_name = name


class Pipeline:
    handler_enabled = "_pipeline_handler_enabled"
    handler_service_name = "_pipeline_service_name"
    handler_filter = "_pipeline_filter"

    def __init__(self, handler):
        self._handler = handler

        # List up all methods with `_msgflow_handler` tag
        #print("List up methods")
        #for method in dir(handler):
        #    print(method)
        #    print(getattr(handler, method))
        #print()

        # List up all methods with `_msgflow_handler` tag
        self._handle_methods = [
            getattr(handler, method) for method in dir(handler)
            if hasattr(getattr(handler, method), self.handler_enabled)
        ]
        print(self._handle_methods)

        services = []

        if isinstance(handler.service, dict):
            # Sort may be needed
            for svc_name, svc in handler.service.items():
                svc.set_name(svc_name)
                services.append(svc)
        elif isinstance(handler.service, list):
            services = handler.service
        else:
            services = [handler.service]

        self._services = services

    async def _handle(self, queue):
        while True:
            msg = await queue.get()
            for method in self._handle_methods:
                handler_enabled, handler_service_name, handler_filter = (
                    getattr(method, self.handler_enabled),
                    getattr(method, self.handler_service_name),
                    getattr(method, self.handler_filter)
                )
                # Logging
                print(f"method: {method.__name__}, enabled: {handler_enabled}, service_name: {handler_service_name}, filter: {str(handler_filter)}")

                if not handler_enabled:
                    continue
                if (handler_service_name is not None) and (msg.service.name != handler_service_name):
                    continue
                if (handler_filter is not None) and (not handler_filter(msg)):
                    continue
                await method(msg)

    async def run(self):
        queue = asyncio.Queue()

        # Create tasks and **schedule to run soon concurrently**
        service_tasks = []
        for service in self._services:
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


def handler(
    _func=None, *,
    service=None,
    cond=None,
    pattern=None,
    pattern_attr=_default_pattern_attr,
):
    """Tag function as a handler of service
    """

    def decorator(func):
        setattr(func, Pipeline.handler_enabled, True)
        setattr(func, Pipeline.handler_service_name, service)
        setattr(func, Pipeline.handler_filter, cond)
        return func

    if _func is None:
        # when handler is called with arguments,,
        # _func is set to None
        return decorator
    else:
        # when handler is called without arguments,
        # _func is set to the function to be decorated
        return decorator(_func)
