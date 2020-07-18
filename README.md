# SmileChat

SmileChat is a simple chatbot framework written in Python for simple configuration, customization and connection with several services.

Documents are available on https://noriyukipy.github.io/smilechat .

## Overview

SmileChat provides following simple and flexible features to develop your chatbot as fast as possible.

- Simple Configuration
- Simple Connection
- Simple Customization

### Simple Configuration

SmileChat adopts YAML-formated configuration file to set up your chatbot.

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

In `service`, you can set up the service which you connect your chatbot.

In`app`, you can specify your core application to generate resposne from a message got from the service defined in `service`.

### Simple Connection

SmileChat provides pupular services as default.
You can just specify each service in YAML configuration file to work with these services.

```yaml
# Slack service
post_service:
  name: pybot.service.SlackService
  config:
    slack_api_token: ${YOUR_TOKEN_HERE}
    channel: ${YOUR_CHANNEL_HERE}
    bot_id: ${YOUR_BOT_ID_HERE}
```

### Simple Customization

SmileChat provides simple and flexible customization architecture to develop your own chatbot.

To implement your custom application, you only need to write you application in a specific-formatted class.

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

Then, the class can be specified in your configuration file.

```
app:
  name: app.MyApp
```

## Getting Started

Let's start working with SmileChat from here https://noriyukipy.github.io/smilechat !

## Building Documents

The document is provided by [MkDocs](https://www.mkdocs.org/) and published by [gh-pages](https://www.npmjs.com/package/gh-pages).

First, build your document to convert markdown files to HTML files.

```sh
$ bash docs_builder.sh build
```

Then built files are placed in `docs/site` .

After checking the content, run `gh-pages` to commit on gh-pages and push to GitHub.

```sh
GIT_USER="Your Name <email@example.com>" bash docs_builder.sh publish
```
