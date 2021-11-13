import datetime
from pydantic import BaseModel
import time
import croniter
from typing import Any, Optional, Dict

import logging
logger = logging.getLogger(__file__)


class CronMessage:
    def __init__(self, text: str):
        """"""
        self._text = text

    @property
    def text(self):
        return self._text

    def respond(self, text):
        raise NotImplementedError()

    @property
    def source(self) -> Any:
        raise NotImplementedError()


class CronConfig(BaseModel):
    cron_format: str
    sleep_interval: int = 1
    num_max_exec: Optional[int] = None


class CronService:
    def __init__(self, config: CronConfig, sleep_func, now_func):
        """
        Args:
            config (Dict[str, Any])
            in_fd (Any)
            out_fd (Any)
        """
        # Validate the cron format
        assert croniter.croniter.is_valid(config.cron_format)

        # Set attributes
        self._config = config
        self._sleep_func = sleep_func
        self._now_func = now_func

    @classmethod
    def from_config(cls, config: Dict[str, object]):
        return cls(
            config=CronConfig(**config),
            sleep_func=time.sleep,
            now_func=datetime.datetime.now,
        )

    def _get_next(self, cron):
        return cron.get_next(ret_type=datetime.datetime)

    def flow(self, bot):
        base = self._now_func()
        cron = croniter.croniter(self._config.cron_format, start_time=base)
        next_time = self._get_next(cron)
        num_exec = 0

        finished = False

        while True:
            if self._config.num_max_exec is not None and self._config.num_max_exec <= 0:
                break
            while True:
                now = self._now_func()
                if now < next_time:
                    break
                logger.info(f'Cron will execute job: cron_format="{self._config.cron_format}", now="{datetime.datetime.isoformat(now)}"')
                msg = CronMessage(text=datetime.datetime.isoformat(next_time))
                bot.handle(message=msg, background=True)
                next_time = self._get_next(cron)
                num_exec += 1

                if (
                    self._config.num_max_exec is not None
                    and num_exec >= self._config.num_max_exec
                ):
                    finished = True
                    break
            if finished:
                break
            self._sleep_func(self._config.sleep_interval)

    def post(self, text):
        raise NotImplementedError()
