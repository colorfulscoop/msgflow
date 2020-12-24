INIT_CONFIG = """
# ===== [Service] =====

# CLI Service
service:
  name: msgflow.service.CliService
  config:
    user_name: you

# Twitter service
#service:
#  name: msgflow.service.TwitterSampleStreamService
#  config:
#    consumer_key: ""
#    consumer_secret: ""
#    access_token_key: ""
#    access_token_secret: ""
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
    def __init__(self, service, config):

        self._service = service

    def handle(self, msg):
        log_msg = f'App got message: Message(text="{msg.text}", conversation_id="{msg.conversation_id}")'
        self._service.post(log_msg)
        msg.respond(f'Thank you for your message "{msg.text}"!')
"""
