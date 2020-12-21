from .protocol import Service


class Controller:
    def __init__(self, service: Service, app):
        self._service = service
        self._app = app

    def start_handle(self):
        for msg in self._service.get_stream():
            self._app.handle(msg)
