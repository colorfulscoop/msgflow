from typing import Protocol


class Message(Protocol):
    @property
    def text(self) -> str:
        return self._text

    def respond(self, text: str) -> None:
        self._api.api_call(
            "chat.postMessage",
            channel=self._config.channel,
            text=f"<@{self._user}> {text}",
            as_user=True,
        )


class Service(Protocol):
    def __init__(self, config: dict[str, str]):
        raise NotImplementedError()

    def get_stream(self) -> list[Message]:
        raise NotImplementedError()

    def post(self, text) -> None:
        raise NotImplementedError()


class App(Protocol):
    def __init__(self, service: Service, config: dict[str, str]):
        raise NotImplementedError()

    def handle(self, message: Message):
        raise NotImplementedError()
