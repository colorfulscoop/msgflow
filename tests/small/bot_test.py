from msgflow.bot import Bot


class MockMessage:
    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text


class MockServicePut:
    def __init__(self, msgs):
        self._msgs = msgs

    def start(self, bot):
        for msg in self._msgs:
            bot.put_msg(msg)


class MockServiceHandle:
    def __init__(self, msgs):
        self._msgs = msgs

    def start(self, bot):
        for msg in self._msgs:
            bot.handle_msg(msg)


class MockApp:
    def __init__(self):
        self.accepted_msg = []

    def handle(self, bot, msg):
        self.accepted_msg.append(msg)


def test_controller_put():
    msgs = [
        MockMessage(text="1"),
        MockMessage(text="2"),
        MockMessage(text="3"),
    ]

    svc = MockServicePut(msgs=msgs)
    app = MockApp()
    controller = Bot(service=svc, post_service=svc, app=app)

    controller.start()

    assert app.accepted_msg == msgs


def test_controller_handle():
    msgs = [
        MockMessage(text="1"),
        MockMessage(text="2"),
        MockMessage(text="3"),
    ]

    svc = MockServiceHandle(msgs=msgs)
    app = MockApp()
    controller = Bot(service=svc, post_service=svc, app=app)

    controller.start()

    assert app.accepted_msg == msgs
