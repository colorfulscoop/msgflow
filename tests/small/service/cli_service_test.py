from msgflow.service import CliService
from msgflow.service.cli_service import CliConfig
from msgflow.bot import Bot
import io


class MockApp:
    def __init__(self):
        self._i = 0

    def handle(self, messenger):
        text = messenger.message.text
        if self._i % 2 == 0:
            messenger.post(text)
        messenger.respond(text)
        self._i += 1


def test_CliService():
    # Prepare Service, App and Bot
    app = MockApp()
    in_fd = io.StringIO("1\n2\n3\n/exit\n")
    out_fd = io.StringIO()
    svc = CliService(config=CliConfig(user_name="you"), in_fd=in_fd, out_fd=out_fd)
    bot = Bot(service=svc, post_service=svc, app=app)

    # Start bot
    bot.start()

    # Assert output
    got = out_fd.getvalue()
    want = "you> 1\nbot> 1\nyou> bot> 2\nyou> 3\nbot> 3\nyou> Bye!\n"
    assert got == want
