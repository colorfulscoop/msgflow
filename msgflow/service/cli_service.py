import sys
from pydantic import BaseModel
from typing import Any


class CliMessage:
    def __init__(self, text: str, user_name: str, out_fd):
        """"""
        self._text = text
        self._user_name = user_name
        self._out_fd = out_fd

    @property
    def text(self):
        return self._text

    @property
    def dialog_id(self) -> str:
        # In CliService, a conversation is identified by the user's name
        return self._user_name

    def respond(self, text):
        fmt = f"bot> {text}"
        print(fmt, file=self._out_fd)

    @property
    def source(self) -> Any:
        raise NotImplementedError()


class CliConfig(BaseModel):
    user_name: str = "you"


class CliService:
    def __init__(self, config: CliConfig, in_fd, out_fd):
        """
        Args:
            config (Dict[str, Any])
            in_fd (Any)
            out_fd (Any)
        """
        # Set attributes
        self._config = config
        self._in_fd = in_fd
        self._out_fd = out_fd

    @classmethod
    def from_config(cls, config: dict[str, object]):
        return cls(config=CliConfig(**config), in_fd=sys.stdin, out_fd=sys.stdout)

    def _show_prompt(self, user_name, out_fd):
        print(f"{user_name}> ", end="", file=out_fd)
        out_fd.flush()

    def flow(self, bot):
        self._show_prompt(self._config.user_name, self._out_fd)
        for line in self._in_fd:
            text = line.rstrip("\n")

            if text == "/exit":
                break

            msg = CliMessage(
                text=text, user_name=self._config.user_name, out_fd=self._out_fd
            )
            bot.handle(msg)
            self._show_prompt(self._config.user_name, self._out_fd)

        # print("", file=self._out_fd)
        print("Bye!", file=self._out_fd)

    def post(self, text):
        print(text, file=self._out_fd)
