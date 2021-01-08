from typing import Protocol


class Message(Protocol):
    @property
    def text(self) -> str:
        raise NotImplementedError()

    @property
    def dialog_id(self) -> str:
        raise NotImplementedError()

    def respond(self, text: str) -> None:
        raise NotImplementedError()


class App(Protocol):
    @classmethod
    def from_config(cls, config: dict[str, object]):
        """
        To initialize App with config defined in YAML configu file,
        the following initializer.
        """
        raise NotImplementedError()

    def handle(self, bot, msg: Message):
        raise NotImplementedError()


class Service(Protocol):
    """Protoocl for Service."""

    @classmethod
    def from_config(cls, config: dict[str, object]):
        raise NotImplementedError()

    def flow(self, bot) -> None:
        raise NotImplementedError()

    def post(self, text) -> None:
        raise NotImplementedError()
