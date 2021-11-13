from pydantic import BaseModel
import time
import logging
from typing import Any, Optional
import re
from typing import Dict, List
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.getLogger(__file__)


class SlackConfigError(Exception):
    """SlackConfigError raises when a config file has wrong settings"""


class SlackMessage:
    def __init__(self, text: str, user: str, say, source):
        """"""
        self._text = text
        self._user = user
        self._say = say
        self._source = source

    @property
    def text(self):
        return self._text

    def respond(self, text):
        self._say(
            text=f"<@{self._user}> {text}",
            # Reply to thread
            thread_ts=self._source.get("thread_ts", self._source["ts"]),
        )


class SlackService:
    def __init__(self, config, app):
        config = config
        self._config = config
        self._app = app

    @classmethod
    def from_config(cls, config: Dict[str, object]):
        cfg = SlackConfig(**config)
        app = App(token=cfg.bot_token)
        return cls(config=cfg, app=app)

    def _build_message(self, message, say):
        regex = r"\s*<@[a-zA-Z0-9]+>\s*"
        return SlackMessage(
            text=re.sub(regex, "", message["text"]),
            user=message["user"],
            say=say,
            source=message,
        )

    def flow(self, bot):
        if self._config.bot_user is None:
            raise SlackConfigError(
                "bot_user should be set when you retrieve messages from Slack"
            )

        def listen_event(message, say, client):
            # https://github.com/slackapi/python-slack-sdk/blob/b22ac3c1f049a5f1385632ccabd144309841dfd4/slack_sdk/web/client.py#L2403
            res = client.conversations_replies(
                channel=message["channel"],
                ts=message.get("thread_ts", message["ts"]),
            )
            context = [self._build_message(message=m, say=say) for m in res["messages"]]
            bot.handle(context=context, background=True)

        regex = f"<@{self._config.bot_user}>"
        self._app.message(regex)(listen_event)

        SocketModeHandler(self._app, self._config.app_token).start()

    def post(self, text):
        if self._config.channel is None:
            raise SlackConfigError("channel should be set when you use post to Slack")
        self._app.client.chat_postMessage(
            channel=self._config.channel,
            text=text,
        )


class SlackConfig(BaseModel):
    app_token: str
    bot_token: str
    bot_user: Optional[str] = None
    channel: Optional[str] = None
