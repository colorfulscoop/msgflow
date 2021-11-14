from queue import Queue
import logging
import threading
from typing import List, Optional
from .protocol import Service
from .protocol import Message
from .protocol import App
from .logging import print_json_log

logger = logging.getLogger(__file__)


class _ProducerClose:
    """"""


class ClosableQueue(Queue):
    _close_obj = _ProducerClose()

    def close(self):
        self.put(self._close_obj)

    def __iter__(self):
        while True:
            item = self.get()
            if item == self._close_obj:
                return
            yield item


def _craete_producer_thread(bot):
    def run():
        # service will return None when it finishes providing messages.
        try:
            _ = bot._service.flow(bot)
        except Exception:
            raise
        finally:
            print_json_log(logger, "debug", "Finish producer thread")
            bot._queue.close()

    t = threading.Thread(target=run, daemon=True)
    return t


def _create_consumer_thread(queue, app):
    def run():
        for msger in queue:
            print_json_log(logger, "debug", f"{queue.qsize()} items in Queue")
            app.handle(msger)
        print_json_log(logger, "debug", "Finish consumer thread")
        return

    t = threading.Thread(target=run, daemon=True)
    return t


class Messenger:
    def __init__(self, message: Message, context: List[Message], post_method):
        self._message = message
        self._context = context
        self._post_method = post_method

    @property
    def message(self) -> Message:
        return self._message

    @property
    def context(self) -> List[Message]:
        return self._context

    def respond(self, *args, **argv):
        return self._message.respond(*args, **argv)

    def post(self, *args, **argv):
        return self._post_method(*args, **argv)


class Bot:
    def __init__(self, service: Service, post_service: Service, app: App):
        self._service = service
        self._post_service = post_service
        self._app = app

        self._queue = ClosableQueue()

    def start(self):
        producer_thread = _craete_producer_thread(self)
        consumer_thread = _create_consumer_thread(queue=self._queue, app=self._app)

        producer_thread.start()
        consumer_thread.start()

        try:
            producer_thread.join()
            consumer_thread.join()
        except KeyboardInterrupt:
            print_json_log(logger, "debug", "Finish main thread")
        except Exception:
            self._queue.close()

    def post(self, text: str):
        self._post_service.post(text=text)

    # Following methods are used in services
    def handle(
        self,
        message: Optional[Message] = None,
        context: List[Message] = [],
        background: bool = False,
    ):

        # Assert argument
        # Only one of msg or context should not be empty
        assert (message and (not context)) or (
            (not message) and context
        ), "Only one of message or context should be not be empty"

        if message:
            context = [message]
        else:
            message = context[0]

        msger = Messenger(
            message=message, context=context, post_method=self._post_service.post
        )

        if background:
            self._queue.put(msger)
        else:
            self._app.handle(msger)
