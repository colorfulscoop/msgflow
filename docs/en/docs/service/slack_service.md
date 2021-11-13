# SlackService

## Config Definition

```sh
class SlackConfig(BaseModel):
    app_token: str
    bot_token: str
    bot_user: Optional[str] = None
    channel: Optional[str] = None
```

## Functions

### Retrieve Messages

To get messages from Slack, you need to set `bot_user`.
Once you set it, you will get messages mentioning to the `bot_user`.

TODO: write how to get bot_user id

```sh
service:
  name: msgflow.service.SlackService
  config:
    app_token: ${APP_TOKEN}
    bot_token: ${BOT_TOKEN}
    bot_user: ${BOT_USER}
```

### Respond to a Message

You can respond to a retrieved message.
The message will be responded in a thread in which the retrieved message exists.

### Post a Message

You need to set `channel` to post a message.

Example of config:

```sh
service:
  name: msgflow.service.SlackService
  config:
    app_token: ${APP_TOKEN}
    bot_token: ${BOT_TOKEN}
    channel: "#random"
```
