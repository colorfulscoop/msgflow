# PyBot

PyBot is a chatbot framework to work with several services (Slack, Twitter, CLI).

## Architecture

Basic architecture to communicate with a service.

```
           get message
         <--------------
    App                    Service
         -------------->
         * respond to message
         * post
```

Use different service depending on respond and post

```
            get message
          <--------------
    App                    Service
     |    -------------->
     |    respond to message
     |
     |------------------>  Service
              post
```


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

## Services

| Name | Description | Stream | Post | Respond to message |
| --- | --- | --- | --- | --- |
| pybot.service.CliService | CLI service to work with stdin and stdout | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| pybot.service.SlackService | Slack service to work with Slack | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| pybot.service.TwitterSampleStreamService | [Twitter sample stream](https://developer.twitter.com/en/docs/tweets/sample-realtime/overview/get_statuses_sample) service to get messages from stream sample | :white_check_mark: | :x: | :x: |