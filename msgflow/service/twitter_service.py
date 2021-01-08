from pydantic import BaseModel
from typing import List
import twitter
import time
import requests
import logging

logging = logging.getLogger(__file__)


class TwitterMessage:
    def __init__(self, status):
        """"""
        self._status = status

    @property
    def text(self):
        return self._text
        return self._status["text"]

    @property
    def dialog_id(self) -> str:
        return self._status.user.screen_name

    def respond(self, text):
        raise NotImplementedError()


class TwitterSampleStreamService:
    def __init__(self, config, api):
        self._config = config
        self._api = api

    @classmethod
    def from_config(cls, config: dict[str, object]):
        cfg = TwitterConfig(**config)
        api = twitter.Api(
            consumer_key=config.consumer_key,
            consumer_secret=config.consumer_secret,
            access_token_key=config.access_token_key,
            access_token_secret=config.access_token_secret,
        )
        return cls(config=cfg, api=api)

    def flow(self, bot):
        while True:
            try:
                need_sleep = False
                for status in self._api.GetStreamSample():
                    if "text" not in status:
                        continue

                    text = status["text"]

                    contains_black_words = False
                    for bwd in self._config.black_words:
                        if bwd in text:
                            contains_black_words = True
                            break
                    if contains_black_words:
                        continue

                    cond = (
                        # Check lang
                        "lang" in status
                        and self._config.lang
                        and status["lang"] == self._config.lang
                        and
                        # Check max_len
                        (
                            (not self._config.max_len)
                            or len(text) <= self._config.max_len
                        )
                    )
                    if cond:
                        bot.handle(TwitterMessage(status=status), background=True)
                        need_sleep = True

                    if need_sleep:
                        time.sleep(self._config.interval)
                        need_sleep = False

            except requests.exceptions.ChunkedEncodingError:
                logging.info("Connection to Twitter was broken." "Reconnect again")

    def post(self, text):
        raise NotImplementedError()


class TwitterConfig(BaseModel):
    consumer_key: str
    consumer_secret: str
    access_token_key: str
    access_token_secret: str
    max_len: int = None
    lang: str = None
    interval: int = None
    black_words: List[str] = []
