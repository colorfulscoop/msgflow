"""
This module implements a service for Twitter mentions timeline.

- Twitter API document: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-mentions_timeline
- Python Twitter document: https://python-twitter.readthedocs.io/en/latest/twitter.html?highlight=since_id#twitter.api.Api.GetMentions
"""

from pydantic import BaseModel
import twitter
import time
import re
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

    def respond(self, text):
        screen_name = self._status.user.screen_name
        msg = f"@{screen_name} {text}"
        in_reply_to = self._status.id
        self._api.PostUpdate(msg, in_reply_to_status_id=in_reply_to)
        logger.info(f"Post update: in_reply_to_status_id={in_reply_to}, text={msg}")


class TwitterMentionsTimelineService:
    def __init__(self, config, api_cls=twitter.Api):
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
        since_id = 1

        # Set the initial since_id
        while True:
            mentions = self._api.GetMentions(since_id=since_id)
            if mentions:
                since_id = mentions[0].id
                logger.info(f"Set initial since_id to {since_id}")
                break
            time.sleep(self._config.interval)

        while True:
            mentions = self._api.GetMentions(since_id=since_id)
            for status in mentions:
                logger.info(f'Get mention: user=@{status.user.screen_name}, status={status.text}')
                yield TwitterMessage(api=self._api, status=status)

            # update since_id
            if mentions:
                since_id = mentions[0].id
                logger.info(f"Update since_id to {since_id}")

            time.sleep(self._config.interval)

    def post(self, text):
        self._api.PostUpdate(text)
        logger.info(f"Post update: text={text}")
