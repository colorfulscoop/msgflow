# CronService

CronService sends messages on a regular basis.

## Install

```sh
$ pip install msgflow[cron]
```

## Config Definition

```py
class CronConfig(BaseModel):
    cron_format: str
    sleep_interval: int = 1
    num_max_exec: Optional[int] = None
```

## Functions

### Retrieve Messages

According to a cron format defined in [croniter](https://github.com/kiorky/croniter), CronService regularly send a message.
A text returned by cronService is a ISO-formatted time (e.g. `2021-11-13T04:38:00` ) .

### Respond to a Message

NotImplemented.

### Post a Message

NotImplemented.

Please use another Service to post a message.

Example of config:

```py
# Send a message every 1 minute
service:
  name: msgflow.service.CronService
  config:
    cron_format: "*/1 * * * *"

# Post a message in your command line
post_service:
  name: msgflow.service.CliService
  config:
    user_name: you
```
