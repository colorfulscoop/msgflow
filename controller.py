class Controller:
    def __init__(self, service, app):
        self._service = service
        self._app = app

    def start_handle(self):
        for msg in self._service.get_stream():
            self._app.handle(msg)
