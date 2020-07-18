from pydantic import BaseModel
from slackclient import SlackClient


class SlackMessage:
    def __init__(self, text, user, api, config):
        """"""
        self._text = text
        self._user = user
        self._config = config
        self._api = api

    @property
    def text(self):
        return self._text

    def respond(self, text):
        self._api.api_call(
            "chat.postMessage",
            channel=self._config.channel,
            text=f"<@{self._user}> {self._text}",
            as_user=True,
        )


class SlackService:
    def __init__(self, config, api_cls=SlackClient):
        config = SlackConfig(**config)
        api = api_cls(
            token=config.slack_api_token,
        )
        self._config = config
        self._api = api

    def get_stream(self):
        con = self._api.rtm_connect()
        if not con:
            raise Exception()

        while True:
            msgs = self._api.rtm_read()
            for msg in msgs:
                if msg["type"] != "message":
                    continue
                text = msg["text"]
                user = msg["user"]
                bot_user = self._config.bot_id

                if bot_user not in text:
                    continue

                text = text.replace(f"<@{bot_user}>", "")

                yield SlackMessage(
                    text=text,
                    user=user,
                    api=self._api,
                    config=self._config,
                )

    def post(self, text):
        self._api.api_call(
            "chat.postMessage",
            channel=self._config.channel,
            text=text,
            as_user=True,
        )


class SlackConfig(BaseModel):
    slack_api_token: str
    channel: str
    bot_id: str
