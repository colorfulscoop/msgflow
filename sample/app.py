class MyApp:
    def __init__(self, service, config):
        """"""
        self._service = service

    def handle(self, message):
        res = f'This is a response to "{message.text}"'
        message.respond(res)
        self._service.post(f'This is a post to "{message.text}"')
