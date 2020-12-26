from msgflow.controller import Controller


class MockMessage:
    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text


class MockService:
    def __init__(self, msgs):
        self._msgs = msgs

    def get_stream(self):
        return self._msgs


class MockApp:
    def __init__(self):
        self.accepted_msg = []

    def handle(self, msg):
        self.accepted_msg.append(msg)


def test_controller():
    msgs = [
        MockMessage(text="1"),
        MockMessage(text="2"),
        MockMessage(text="3"),
    ]

    svc = MockService(msgs=msgs)
    app = MockApp()
    controller = Controller(service=svc, app=app)

    controller.start()

    assert app.accepted_msg == msgs
