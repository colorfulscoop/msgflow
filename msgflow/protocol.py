from typing import Protocol


class Message(Protocol):
    @property
    def text(self) -> str:
        raise NotImplementedError()

    @property
    def conversation_id(self) -> str:
        raise NotImplementedError()

    def respond(self, text: str) -> None:
        raise NotImplementedError()


class Service(Protocol):
    """Protoocl for Service.

    To initialize Service with config defined in YAML configu file,
    you need to implement the following initializer.

        def __init__(self, config: dict[str, str]):
            raise NotImplementedError()
    """

    def get_stream(self) -> list[Message]:
        raise NotImplementedError()

    def post(self, text) -> None:
        raise NotImplementedError()


class App(Protocol):
    """Protoocl for App.

    To initialize App with config defined in YAML configu file,
    the following initializer.

        def __init__(self, service: Service, config: dict[str, str]):
            raise NotImplementedError()
    """

    def handle(self, msg: Message):
        raise NotImplementedError()
