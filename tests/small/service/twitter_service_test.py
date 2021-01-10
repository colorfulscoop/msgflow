from msgflow.service import TwitterSampleStreamService
from msgflow.service.twitter_service import TwitterConfig
from msgflow.bot import Bot


class MockTwitterApi:
    def get_sample_stream(self):
        tweets = [
            {'id': '0', 'text': 'test0', 'lang': 'ja'},
            {'id': '1', 'text': 'test1', 'lang': 'ja'},
            {'id': '2', 'text': 'test2', 'lang': 'ja'},
            {'id': '3', 'text': 'test3_long_sentence', 'lang': 'ja'},
            {'id': '4', 'text': 'test4_black_words', 'lang': 'ja'},
            {'id': '4', 'text': 'test4_diff_lang', 'lang': 'en'},
            {'id': '5', 'text': 'test5', 'lang': 'ja'},
        ]
        for item in tweets:
            yield item


class MockApp:
    def __init__(self):
        self._recieved = []

    def handle(self, bot, msg):
        self._recieved.append(msg)


class MockSleepCond:
    def __init__(self):
        self._now = 0

    def reset(self):
        self._now = 0

    def step(self):
        self._now += 1

    def need_sleep(self, interval):
        return self._now <= interval


def test_TwitterSampleStreamService_flow():
    api = MockTwitterApi()
    config = TwitterConfig(bearer_token="", max_len=5, lang="ja", black_words=["4"], interval=1)
    sleep_cond = MockSleepCond()

    svc = TwitterSampleStreamService(config=config, api=api, sleep_cond=sleep_cond)
    app = MockApp()
    bot = Bot(service=svc, post_service=svc, app=app)

    # Start bot
    bot.start()

    # Assert
    assert [item.text for item in app._recieved] == ["test1", "test5"]