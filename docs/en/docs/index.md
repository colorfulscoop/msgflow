# msgFlow

[msgFlow](https://github.com/noriyukipy/msgflow) is a simple chatbot framework written in Python for simple configuration, customization and connection with several services.

msgFlow provides following simple and flexible features to develop your chatbot as fast as possible.

- Simple Configuration
- Simple Connection
- Simple Customization

## Simple Configuration

msgFlow adopts YAML-formated configuration file to set up your chatbot.

```yaml
# Service to connect
service:
  name: msgflow.service.CliService
  config:
    user_name: you

# Application to generate response
app:
  name: app.MyApp
```

In `service`, you can set up the service which you connect your chatbot.

In`app`, you can specify your core application to generate resposne from a message got from the service defined in `service`.

## Simple Connection

msgFlow provides pupular services as default.
You can just specify each service in YAML configuration file to work with these services.

```yaml
# Slack service
post_service:
  name: msgflow.service.SlackService
  config:
    slack_api_token: ${YOUR_TOKEN_HERE}
    channel: ${YOUR_CHANNEL_HERE}
    bot_id: ${YOUR_BOT_ID_HERE}
```

## Simple Customization

msgFlow provides simple and flexible customization architecture to develop your own chatbot.

To implement your custom application, you only need to write you application in a specific-formatted class.

```py
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
```

Then, the class can be specified in your configuration file.

```yaml
app:
  name: app.MyApp
```
