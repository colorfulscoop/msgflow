"""
This module implements a service for Twitter mentions timeline.

- Twitter API document: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-mentions_timeline
- Python Twitter document: https://python-twitter.readthedocs.io/en/latest/twitter.html?highlight=since_id#twitter.api.Api.GetMentions
"""

from pydantic import BaseModel
import twitter
import time
import re
import requests
import logging

logger = logging.getLogger(__file__)


class TwitterConfig(BaseModel):
    consumer_key: str
    consumer_secret: str
    access_token_key: str
    access_token_secret: str
    interval: int = None


class TwitterMessage:
    def __init__(self, api, status):
        """"""
        self._api = api
        self._status = status

    @property
    def text(self):
        text = self._status.text
        text = re.sub(r"\s*@[a-zA-Z0-9_]+\s*", "", text)
        return text

    @property
    def dialog_id(self) -> str:
        return self._status.user.screen_name

    def respond(self, text):
        screen_name = self._status.user.screen_name
        msg = f"@{screen_name} {text}"
        in_reply_to = self._status.id
        try:
            self._api.PostUpdate(msg, in_reply_to_status_id=in_reply_to)
            logger.info(f"Post update: in_reply_to_status_id={in_reply_to}, text={msg}")
        except requests.exceptions.ConnectionError as err:
            logger.exception(f"Post update error: %s", err)


class TwitterMentionsTimelineService:
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
        since_id = 1

        # Set the initial since_id
        while True:
            try:
                mentions = self._api.GetMentions(since_id=since_id)
            except requests.exceptions.ConnectionError as err:
                logger.exception(f"twitter.GetMentions error: %s", err)
                time.sleep(self._config.interval)
                continue

            if mentions:
                since_id = mentions[0].id
                logger.info(f"Set initial since_id to {since_id}")
                break
            time.sleep(self._config.interval)

        while True:
            try:
                mentions = self._api.GetMentions(since_id=since_id)
            except requests.exceptions.ConnectionError as err:
                logger.exception(f"twitter.GetMentions error: %s", err)
                time.sleep(self._config.interval)
                continue

            for status in mentions:
                logger.info(
                    f"Get mention: user=@{status.user.screen_name}, status={status.text}"
                )
                bot.handle(
                    TwitterMessage(api=self._api, status=status), background=True
                )

            # update since_id
            if mentions:
                since_id = mentions[0].id
                logger.info(f"Update since_id to {since_id}")

            time.sleep(self._config.interval)

    def post(self, text):
        try:
            self._api.PostUpdate(text)
            logger.info(f"Post update: text={text}")
        except requests.exceptions.ConnectionError as err:
            logger.exception(f"twitter.PostUpdate error: %s", err)
