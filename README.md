# PyBot

PyBot is a chatbot framework to work with several services (Slack, Twitter, CLI).

## Installation

```sh
$ pip install git+https://github.com/noriyukipy/pybot
```

## Usage

Change directory to `sample` and run `pybot.main`.

```sh
$ python -m pybot.main --config_file=config.yml
INFO:root:"post_service" is not defined in config file. "service" is used for "post_service" instead.
you> Hi
bot> This is a response to "Hi"
This is a post to "Hi"
you>
```