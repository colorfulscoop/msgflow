# Getting Started

msgFlow is a chatbot framework to work with several services (Slack, Twitter, CLI).

## Installation

```sh
$ pip install git+https://github.com/noriyukipy/msgflow
```

## Your First App

To run your chatbot, msgFlow requires config and app files.
`init` provides you default config and app files.

To place these files, create working directory first and change directory there.

```sh
$ mkdir work
$ cd work
```

Then run `init` command to generate default config and app templates.

```sh
$ python -m msgflow.main init
$ ls -1
app.py
config.yml
```

Then execute `run` command which enables you to talk with msgFlow via stdin/stdout.

```sh
$ python -m msgflow.main run --config_file=config.yml
INFO:root:"post_service" is not defined in config file. "service" is used for "post_service" instead.
you> Hi
bot> This is a response to "Hi"
This is a post to "Hi"
you>
```

## Services

| Name | Description | Stream | Post | Respond to message |
| --- | --- | --- | --- | --- |
| msgflow.service.CliService | CLI service to work with stdin and stdout | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| msgflow.service.SlackService | Slack service to work with Slack | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| msgflow.service.TwitterSampleStreamService | [Twitter sample stream](https://developer.twitter.com/en/docs/tweets/sample-realtime/overview/get_statuses_sample) service to get messages from sample stream | :white_check_mark: | :x: | :x: |

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
