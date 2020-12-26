from queue import Queue
import logging
import threading
from .protocol import Service
from .protocol import App
from .logging import print_json_log

logger = logging.getLogger(__file__)


class _ProducerClose:
    """"""


def _craete_producer_thread(que, service):
    def run():
        for msg in service.get_stream():
            que.put(msg)

        que.put(_ProducerClose())
        print_json_log(logger, "debug", "Finish producer thread")

    t = threading.Thread(target=run, daemon=True)
    return t


def _create_consumer_thread(que, app):
    def run():
        while True:
            msg = que.get()
            if type(msg) == _ProducerClose:
                print_json_log(
                    logger, "debug", "Got _ProducerClose message from producer thread"
                )
                print_json_log(logger, "debug", "Finish consumer thread")
                return
            app.handle(msg)

    t = threading.Thread(target=run, daemon=True)
    return t


class Controller:
    def __init__(self, service: Service, app: App):
        self._service = service
        self._app = app

    def start(self):
        que = Queue()

        producer_thread = _craete_producer_thread(que, self._service)
        consumer_thread = _create_consumer_thread(que, self._app)

        producer_thread.start()
        consumer_thread.start()

        try:
            consumer_thread.join()
        except KeyboardInterrupt:
            print_json_log(logger, "debug", "Finish main thread")
            return
