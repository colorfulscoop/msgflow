from pydantic import BaseModel
from typing import List
import twitter
import time
import requests
import logging

logging = logging.getLogger(__file__)


class TwitterMessage:
    def __init__(self, text):
        """"""
        self._text = text

    @property
    def text(self):
        return self._text

    def respond(self, text):
        raise NotImplementedError()


class TwitterSampleStreamService:
    def __init__(self, config, api_cls=twitter.Api):
        """
        Args:
            config (Dict[str, Any])
            in_fd (Any)
            out_fd (Any)
        """
        config = TwitterConfig(**config)
        api = api_cls(
            consumer_key=config.consumer_key,
            consumer_secret=config.consumer_secret,
            access_token_key=config.access_token_key,
            access_token_secret=config.access_token_secret,
        )

        self._config = config
        self._api = api

    def get_stream(self):
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
                        yield TwitterMessage(text=text)
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
