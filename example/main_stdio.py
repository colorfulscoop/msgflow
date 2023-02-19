import asyncio
import msgflow
from msgflow.channel.stdio_channel import StdioChannel


class App:
    def __init__(self):
        self._channel = StdioChannel(user_name="You")

    @property
    def input_channel(self):
        return self._channel

    @msgflow.handler(
        pattern=r'^Hello$',
        pattern_attr=lambda msg: msg.req,
    )
    async def handle_input(self, msg, match):
        await msg.respond(f"Hello!, match={match.group()}")


def main():
    app = App()
    bot = msgflow.Pipeline(app=app)
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("Exit by KeyboardInterrupt")


main()
