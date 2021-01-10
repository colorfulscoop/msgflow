import datetime
from pydantic import BaseModel
import time
import croniter
from typing import Any


class CronMessage:
    def __init__(self, text: str):
        """"""
        self._text = text

    @property
    def text(self):
        return self._text

    @property
    def dialog_id(self) -> str:
        # In CliService, a conversation is identified by the user's name
        return self._text

    def respond(self, text):
        raise NotImplementedError()

    @property
    def source(self) -> Any:
        raise NotImplementedError()


class CronConfig(BaseModel):
    cron_format: str
    sleep_interval: int = 1
    num_max_exec: int = 0


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
    def from_config(cls, config: dict[str, object]):
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
            while True:
                now = self._now_func()
                print(now)
                if now < next_time:
                    print("Break", now)
                    break
                msg = CronMessage(text=str(next_time))
                bot.handle(msg=msg, background=True)
                next_time = self._get_next(cron)
                num_exec += 1
                print("Num_exec", num_exec, self._config.num_max_exec)

                if (
                    self._config.num_max_exec > 0
                    and num_exec >= self._config.num_max_exec
                ):
                    finished = True
                    break
            if finished:
                break
            self._sleep_func(self._config.sleep_interval)
            print("Sleep")

    def post(self, text):
        raise NotImplementedError()
