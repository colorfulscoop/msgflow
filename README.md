# msgFlow

![](https://github.com/noriyukipy/msgflow/workflows/unittest/badge.svg)

[msgFlow](https://github.com/noriyukipy/msgflow) is a simple chatbot framework written in Python for simple configuration, customization and connection with several services.

## Installation

Prepare Python >= 3.9. Then install msgFlow from GitHub.

```sh
$ pip install git+https://github.com/noriyukipy/msgflow
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
INFO:/usr/local/lib/python3.9/site-packages/msgflow/main.py:"post_service" is not defined in config file. "service" is used for "post_service" instead.
INFO:/usr/local/lib/python3.9/site-packages/msgflow/main.py:service: CliService
INFO:/usr/local/lib/python3.9/site-packages/msgflow/main.py:post_service: CliService
you>
```

The prompt `you>` waits for your input. Input your utterance there.

```sh
you> Hello
App got message: Message(text="Hello", conversation_id="you")
bot> Thank you for your message "Hello"!
you> World
App got message: Message(text="World", conversation_id="you")
bot> Thank you for your message "World"!
```

The default App class shows the message that what kind of message was reached, and then return the response with your input utterance.

To finish the conversation, input `<Ctr-D>` or `<Ctr-C>`.

```sh
you>
Bye!
```

## How It Works

As you saw in the previous section, msgFlow requires two types of files to run.

One is the configuration file. The`config.yml` file which the `init` command generates is the configuration file.

The other is a Python script which defines the `App` class.


## Service

| Name | Description | Stream | Post | Respond to message |
| --- | --- | --- | --- | --- |
| msgflow.service.CliService | CLI service to work with stdin and stdout | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| msgflow.service.SlackService | Slack service to work with Slack | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| msgflow.service.TwitterSampleStreamService | [Twitter sample stream](https://developer.twitter.com/en/docs/tweets/sample-realtime/overview/get_statuses_sample) service to get messages from sample stream | :white_check_mark: | :x: | :x: |
| msgflow.service.TwitterMentionsTimeline | [Twitter mentions timeline](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-mentions_timeline) service to get messages from mentions timeline | :white_check_mark: | :white_check_mark: | :white_check_mark: |
