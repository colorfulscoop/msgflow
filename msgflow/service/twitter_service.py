from pydantic import BaseModel
from typing import List
import requests
import logging
import json
import datetime
from typing import Any
from msgflow.logging import print_json_log

logger = logging.getLogger(__file__)


class TwitterMessage:
    def __init__(self, status):
        """"""
        self._status = status

    @property
    def text(self):
        return self._status["text"]

    @property
    def dialog_id(self) -> str:
        return self._status["conversation_id"]

    @property
    def source(self) -> Any:
        return self._status

    def respond(self, text):
        raise NotImplementedError()


class _TwitterApi:
    def __init__(self, bearer_token):
        self._bearer_token = bearer_token

    def get_sample_stream(self):
        try:
            res = requests.get(
                url="https://api.twitter.com/2/tweets/sample/stream",
                params={
                    "tweet.fields": "lang,conversation_id",
                },
                headers={"Authorization": f"Bearer {self._bearer_token}"},
                stream=True,
            )

            # Use iter_lines and decode_unicode to iterate streaming output
            # Check the details in the document
            # https://2.python-requests.org/projects/3/user/advanced/#streaming-requests
            for item in res.iter_lines(decode_unicode=True):
                # Output looks like
                #  {"data": {"id": "...", "text": "..."}}
                try:
                    yield (json.loads(item)["data"])
                except json.decoder.JSONDecodeError:
                    # line sometimes b'', which raises error
                    print_json_log(logger, "info", f"{item} cannot be decoded as dict")
        except requests.exceptions.ChunkedEncodingError:
            print_json_log(
                logger, "info", "Connection to Twitter was broken." "Reconnect again"
            )


class _SleepCondition:
    def __init__(self):
        self._start_at = datetime.datetime.now()
        self._now = datetime.datetime.now()

    def reset(self):
        self._start_at = datetime.datetime.now()
        self._now = datetime.datetime.now()

    def step(self):
        self._now = datetime.datetime.now()

    def need_sleep(self, interval):
        return self._now - self._start_at <= datetime.timedelta(seconds=interval)


class TwitterSampleStreamService:
    def __init__(self, config, api, sleep_cond):
        self._config = config
        self._api = api
        self._sleep_cond = sleep_cond

    @classmethod
    def from_config(cls, config: dict[str, object]):
        cfg = TwitterConfig(**config)
        api = _TwitterApi(bearer_token=cfg.bearer_token)
        return cls(config=cfg, api=api, sleep_cond=_SleepCondition())

    def flow(self, bot):
        self._sleep_cond.reset()
        for status in self._api.get_sample_stream():
            # Update sleep condition
            self._sleep_cond.step()

            # Check sleep condition
            if self._sleep_cond.need_sleep(self._config.interval):
                continue
            assert "text" in status
            assert "lang" in status

            text = status["text"]

            # Check blackwords condition
            contains_black_words = False
            for bwd in self._config.black_words:
                if bwd in text:
                    contains_black_words = True
                    break
            if contains_black_words:
                continue

            cond = (
                # Check lang
                self._config.lang
                and status["lang"] == self._config.lang
                and
                # Check max_len
                (self._config.max_len and len(text) <= self._config.max_len)
            )
            if cond:
                bot.handle(TwitterMessage(status=status), background=True)
                self._sleep_cond.reset()

    def post(self, text):
        raise NotImplementedError()


class TwitterConfig(BaseModel):
    bearer_token: str
    max_len: int = None
    lang: str = None
    interval: int = None
    black_words: List[str] = []
