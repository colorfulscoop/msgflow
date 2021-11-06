from msgflow.service import CronService
from msgflow.service.cron_service import CronConfig
from msgflow.bot import Bot
import datetime


class MockApp:
    def handle(self, messenger):
        messenger.post(messenger.message.text)


class MockSleeper:
    def __init__(self):
        self.record = []

    def sleep(self, time):
        self.record.append(time)


class MockDatetime:
    def __init__(self, times):
        self._times = times
        self._i = 0

    def now(self):
        t = self._times[self._i]
        self._i += 1
        return t


class MockPostService:
    def __init__(self):
        self.record = []

    def post(self, text):
        self.record.append(text)

    def flow(self, bot):
        raise NotImplementedError()


def test_CliService():
    # Prepare Service, App and Bot
    app = MockApp()
    cron_format = "* * * * * */2"  # Run every 2 seconds
    sleeper = MockSleeper()
    dt = MockDatetime([datetime.datetime(2021, 1, 1, 0, 0, i) for i in range(59)])
    svc = CronService(
        config=CronConfig(cron_format=cron_format, sleep_interval=1, num_max_exec=3),
        sleep_func=sleeper.sleep,
        now_func=dt.now,
    )
    post_svc = MockPostService()
    bot = Bot(service=svc, post_service=post_svc, app=app)

    # Start bot
    bot.start()

    # Assert output
    assert sleeper.record == [1, 1, 1]
    assert post_svc.record == [
        "2021-01-01 00:00:02",
        "2021-01-01 00:00:04",
        "2021-01-01 00:00:06",
    ]
