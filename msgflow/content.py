INIT_CONFIG = """
# ===== [Service] =====

# CLI Service
service:
  name: msgflow.service.CliService
  config:
    user_name: you


# ===== [Post Service] =====
# If you want to use different service to post your message,
# define post service.

#post_service:
#  name: msgflow.service.CliService
#  config:
#    user_name: you


# ===== [App] =====
# Define your app here

app:
  name: app.MyApp
"""


INIT_APP = """
from typing import Dict
from msgflow import Messenger


class MyApp:
    def __init__(self):
        pass

    @classmethod
    def from_config(cls, config: Dict[str, object]):
        return cls()

    def handle(self, messenger: Messenger):
        log_msg = f'App got message: Message(text="{messenger.message.text}", context="{[m.text for m in messenger.context]}")'
        messenger.post(log_msg)
        messenger.respond(f'Thank you for your message "{messenger.message.text}"!')
"""
