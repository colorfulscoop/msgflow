import sys
from pydantic import BaseModel


class CliMessage:
    def __init__(self, text):
        """"""
        self._text = text

    @property
    def text(self):
        return self._text

    def respond(self, text):
        fmt = f"bot> {text}"
        print(fmt)


class CliService:
    def __init__(self, config):
        """
        Args:
            config (Dict[str, Any])
            in_fd (Any)
            out_fd (Any)
        """
        # Set attributes
        self._config = CliConfig(**config)
        self._in_fd = sys.stdin
        self._out_fd = sys.stdout

    def get_stream(self):
        while True:
            try:
                text = input(f"{self._config.user_name}> ")
            except EOFError:
                # When user inputs EOF (<CTRL>-D), return stream
                return

            yield CliMessage(text=text)

    def post(self, text):
        print(text, file=self._out_fd)


class CliConfig(BaseModel):
    user_name: str = "you"
