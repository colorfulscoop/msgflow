import sys
from pydantic import BaseModel


class CliMessage:
    def __init__(self, text, service):
        """"""
        self._text = text
        self._service = service

    @property
    def text(self):
        return self._text

    def respond(self, text):
        return self._service.respond(self, text)


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
        for line in self._in_fd:
            text = line.strip("\n")
            yield CliMessage(text=text, service=self)

    def post(self, text):
        print(text, file=self._out_fd)

    def respond(self, message, text):
        user_name = self._config.user_name
        fmt = f"@{user_name} {text}"
        print(fmt, file=self._out_fd)


class CliConfig(BaseModel):
    user_name: str = "you"
