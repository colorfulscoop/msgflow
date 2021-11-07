from msgflow.bot import Bot
from typing import Any
import pytest


class MockMessage:
    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text

    def respond(self, text: str) -> None:
        raise NotImplementedError()

    @property
    def source(self) -> Any:
        raise NotImplementedError()

    def __eq__(self, other):
        return self._text == other.text


class MockService:
    def __init__(self, msgs, background):
        self._msgs = msgs
        self._background = background

    def flow(self, bot):
        for message, context in self._msgs:
            bot.handle(message=message, context=context, background=self._background)

    def post(self, text):
        raise NotImplementedError()


class MockApp:
    def __init__(self):
        self.accepted_msg = []
        self.accepted_context = []

    def handle(self, msger):
        self.accepted_msg.append(msger.message)
        self.accepted_context.append(msger.context)


def test_start():
    msgs = [
        (MockMessage(text="1"), []),
        (MockMessage(text="2"), []),
        (MockMessage(text="3"), []),
    ]

    for background in [False, True]:
        svc = MockService(msgs=msgs, background=background)
        app = MockApp()
        bot = Bot(service=svc, post_service=svc, app=app)
        bot.start()

        assert app.accepted_msg == [
            MockMessage(text="1"),
            MockMessage(text="2"),
            MockMessage(text="3"),
        ]
        assert app.accepted_context == [
            [MockMessage(text="1")],
            [MockMessage(text="2")],
            [MockMessage(text="3")],
        ]


def test_start_with_context():
    msgs = [
        (None, [MockMessage(text="1"), MockMessage(text="2")]),
        (None, [MockMessage(text="2"), MockMessage(text="3")]),
        (None, [MockMessage(text="3"), MockMessage(text="4")]),
    ]

    svc = MockService(msgs=msgs, background=False)
    app = MockApp()
    bot = Bot(service=svc, post_service=svc, app=app)
    bot.start()

    expected = [
        [MockMessage(text="1"), MockMessage(text="2")],
        [MockMessage(text="2"), MockMessage(text="3")],
        [MockMessage(text="3"), MockMessage(text="4")],
    ]
    assert app.accepted_context == expected


def test_handle_error_giving_both_message_and_context():
    message = [MockMessage(text="1")]
    context = [[MockMessage(text="1")]]
    bot = Bot(service=None, post_service=None, app=None)

    with pytest.raises(AssertionError):
        bot.handle(message=message, context=context)


def test_handle_error_giving_both_message_and_context_empty():
    bot = Bot(service=None, post_service=None, app=None)

    with pytest.raises(AssertionError):
        bot.handle()
