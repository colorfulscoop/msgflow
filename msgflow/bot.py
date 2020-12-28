from queue import Queue
import logging
import threading
from .protocol import Service
from .protocol import Message
from .protocol import App
from .logging import print_json_log

logger = logging.getLogger(__file__)


class _ProducerClose:
    """"""


def _craete_producer_thread(bot):
    def run():
        # service will return None when it finishes providing messages.
        _ = bot._service.flow(bot)
        bot._queue.put(_ProducerClose())
        print_json_log(logger, "debug", "Finish producer thread")

    t = threading.Thread(target=run, daemon=True)
    return t


def _create_consumer_thread(bot):
    def run():
        while True:
            msg = bot._queue.get()
            print_json_log(logger, "debug", f"{bot._queue.qsize()} items in Queue")
            if type(msg) == _ProducerClose:
                print_json_log(
                    logger, "debug", "Got _ProducerClose message from producer thread"
                )
                print_json_log(logger, "debug", "Finish consumer thread")
                return
            bot.handle(msg)

    t = threading.Thread(target=run, daemon=True)
    return t


class Bot:
    def __init__(self, service: Service, post_service: Service, app: App):
        self._service = service
        self._post_service = post_service
        self._app = app

        self._queue = Queue()

    def start(self):
        producer_thread = _craete_producer_thread(self)
        consumer_thread = _create_consumer_thread(self)

        producer_thread.start()
        consumer_thread.start()

        try:
            producer_thread.join()
            consumer_thread.join()
        except KeyboardInterrupt:
            print_json_log(logger, "debug", "Finish main thread")
            return

    def post(self, text: str):
        self._post_service.post(text=text)

    # Following methods are used in services
    def handle(self, msg: Message, background: bool = False):
        if background:
            self._queue.put(msg)
        else:
            self._app.handle(bot=self, msg=msg)
