from pydantic import BaseModel
import time
import re
import requests
import logging

logger = logging.getLogger(__file__)


class _TwitterApi:
    def __init__(self, bearer_token):
        self._bearer_token = bearer_token

    def post_update(self, text, in_reply_to_status_id):
        """This method will be implemented in the future once Twitter implements PostUpdate API in v2."""

    def get_mentions(self, user_id, since_id):
        """

        user_id can be found by querying

            curl -X GET -H "Authorization: Bearer $BEARER_TOKEN" "https://api.twitter.com/2/users/by?usernames=your_user_name"

        """
        res = requests.get(
            url=f"https://api.twitter.com/2/users/{user_id}/mentions",
            params={
                "since_id": since_id,
            },
            headers={"Authorization": f"Bearer {self._bearer_token}"},
        )
        return res.json()["data"]


class TwitterConfig(BaseModel):
    user_id: str  # Required to get mentions timeline
    bearer_token: str
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
            consumer_key=cfg.consumer_key,
            consumer_secret=cfg.consumer_secret,
            access_token_key=cfg.access_token_key,
            access_token_secret=cfg.access_token_secret,
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
