# SlackService

SlackService connects to Slack via [Socket Mode](https://api.slack.com/apis/connections/socket).

SlackService enables you to

* retrive mentions
* respond to a message in a same thread
* post a message to a channel

## Install

```sh
$ pip install msgflow[slack]
```

## Config Definition

```py
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

```py
service:
  name: msgflow.service.SlackService
  config:
    app_token: ${APP_TOKEN}
    bot_token: ${BOT_TOKEN}
    bot_user: ${BOT_USER}
```

### Respond to a Message

You can respond to a retrieved message.
The message will be responded in the same thread as the original message.

### Post a Message

You need to set `channel` to post a message.

Example of config:

```py
service:
  name: msgflow.service.SlackService
  config:
    app_token: ${APP_TOKEN}
    bot_token: ${BOT_TOKEN}
    channel: "#random"
```
