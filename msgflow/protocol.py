from typing import Protocol


class Message(Protocol):
    @property
    def text(self) -> str:
        raise NotImplementedError()

    def respond(self, text: str) -> None:
        raise NotImplementedError()


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
