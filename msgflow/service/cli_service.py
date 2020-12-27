import sys
from pydantic import BaseModel


class CliMessage:
    def __init__(self, text: str, user_name: str):
        """"""
        self._text = text
        self._user_name = user_name

    @property
    def text(self):
        return self._text

    @property
    def conversation_id(self) -> str:
        # In CliService, a conversation is identified by the user's name
        return self._user_name

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

    def start_msg_stream(self, bot):
        while True:
            try:
                text = input(f"{self._config.user_name}> ")
                msg = CliMessage(text=text, user_name=self._config.user_name)
                bot.handle(msg)
            except (EOFError, KeyboardInterrupt):
                # When user inputs EOF (<CTRL>-D), saye hello good bye and exit stream
                print("Bye!")
                return

    def post(self, text):
        print(text, file=self._out_fd)


class CliConfig(BaseModel):
    user_name: str = "you"
