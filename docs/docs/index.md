# SmileChat - Simple Chatbot Framework

## Simple Configuration

```yaml
# Service to connect
service:
  name: pybot.service.CliService
  config:
    user_name: you

# Application to generate response
app:
  name: app.MyApp
```

## Simple Customization

```py
class MyApp:
    def __init__(self, service, config):
        """"""
        self._service = service

    def handle(self, message):
        res = f'{message.text}'
        message.respond(res)
        self._service.post(f'Log: "{message.text}"')
```

## Simple Connection

```yaml
# Slack service
post_service:
  name: pybot.service.SlackService
  config:
    slack_api_token: ${YOUR_TOKEN_HERE}
    channel: ${YOUR_CHANNEL_HERE}
    bot_id: ${YOUR_BOT_ID_HERE}
```
