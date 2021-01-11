# msgFlow

![](https://github.com/colorfulscoop/msgflow/workflows/unittest/badge.svg)

[msgFlow](https://github.com/colorfulscoop/msgflow) is a simple chatbot framework written in Python for simple configuration, customization and connection with several services.

## Installation

Prepare Python >= 3.9. Then install msgFlow from PyPI.

```sh
$ pip install msgflow
```

msgFlow separas dependent libraries for each service. To make all the services available, install msgFlow with the following options.

```sh
$ pip install msgflow[webapi,twitter,slack]
```

## Quick Start

msgFlow requires a configuration file and an App script to run.
To create those files, create your working directory first.

```sh
$ mkdir work
$ cd work/
```

msgFlow provides `init` command to generate the configuratio file and App script for you.

```sh
$ python -m msgflow.main init
$ ls
app.py  config.yml
```

Configuration file tells msgFlow which service is used to get inputs and return the response. and which App class is used.
The App script defines the App class which defines how to generate a response from the input.

As a default, Config file uses stdin to get the input and show the output in the stdout.

Let us run the msgFlow with the Config setting.
You can utilize the `run` command with `--config_file` option which specify the default config file.

```sh
$ python -m msgflow.main run --config_file config.yml
INFO:/work/msgflow/main.py:{"level": "info", "message": {"service": "CliService", "post_service": "CliService"}, "time": "2020-12-26 11:10:43.886375"}
```

The prompt `you>` waits for your input. Input your utterance there.

```sh
you> Hello
App got message: Message(text="Hello", dialog_id="you")
bot> Thank you for your message "Hello"!
you> World
App got message: Message(text="World", dialog_id="you")
bot> Thank you for your message "World"!
```

The default App class shows the message that what kind of message was reached, and then return the response with your input utterance.

To finish the conversation, input `/exit`.

```sh
you> /exit
Bye!
```

## Service List

| Name | Description | Flow message | Post | Respond to message | Where to handle message |
| --- | --- | --- | --- | --- | --- |
| msgflow.service.CliService | Service to get input from stdin and output to stdout | o | o| o | Foreground |
| msgflow.service.CronService | Service to post on a regular basis | o  | | | Foreground |
| msgflow.service.WebapiService | Service to serve web API | o | | o  | Foreground |
| msgflow.service.SlackService | Service to work with Slack | o | o | o | Background |
| msgflow.service.TwitterSampleStreamService | This service gets tweets via [Twitter sampled stream v2](https://developer.twitter.com/en/docs/twitter-api/tweets/sampled-stream/api-reference/get-tweets-sample-stream) | o | | | Background |

o: available, blank: unavailable