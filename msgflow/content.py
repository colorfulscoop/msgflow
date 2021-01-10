INIT_CONFIG = """
# ===== [Service] =====

# CLI Service
service:
  name: msgflow.service.CliService
  config:
    user_name: you

# Webapi Service
#service:
#  name: msgflow.service.WebapiService
#  config:
#    host: 0.0.0.0
#    port: 8080

# Twitter sample stream service
#service:
#  name: msgflow.service.TwitterSampleStreamService
#  config:
#    bearer_token: ""
#    lang: ja
#    max_len: 50
#    interval: 10

# Slack service
#service:
#  name: msgflow.service.SlackService
#  config:
#    slack_api_token: ""
#    channel: ""
#    bot_id: ""


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
class MyApp:
    def __init__(self):
        pass

    @classmethod
    def from_config(cls, config: dict[str, object]):
        return cls()

    def handle(self, bot, msg):
        log_msg = f'App got message: Message(text="{msg.text}", dialog_id="{msg.dialog_id}")'
        bot.post(log_msg)
        msg.respond(f'Thank you for your message "{msg.text}"!')
"""
