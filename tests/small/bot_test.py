from msgflow.bot import Bot


class MockMessage:
    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text


class MockService:
    def __init__(self, msgs):
        self._msgs = msgs

    def flow(self, bot):
        for msg in self._msgs:
            bot.handle(msg=msg)


class MockServiceBackground:
    def __init__(self, msgs):
        self._msgs = msgs

    def flow(self, bot):
        for msg in self._msgs:
            bot.handle(msg=msg, background=True)


class MockApp:
    def __init__(self):
        self.accepted_msg = []

    def handle(self, bot, msg):
        self.accepted_msg.append(msg)


def test_controller():
    msgs = [
        MockMessage(text="1"),
        MockMessage(text="2"),
        MockMessage(text="3"),
    ]

    svc = MockService(msgs=msgs)
    app = MockApp()
    controller = Bot(service=svc, post_service=svc, app=app)

    controller.start()

    assert app.accepted_msg == msgs


def test_controller_background():
    msgs = [
        MockMessage(text="1"),
        MockMessage(text="2"),
        MockMessage(text="3"),
    ]

    svc = MockServiceBackground(msgs=msgs)
    app = MockApp()
    controller = Bot(service=svc, post_service=svc, app=app)

    controller.start()

    assert app.accepted_msg == msgs
