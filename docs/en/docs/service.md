# Service

| Name | Description | Retrieve Messages | Respond to a Message | Post a Message |
| --- | --- | --- | --- | --- | --- |
| msgflow.service.CliService | Get messages from from stdin and output to stdout | o | o | o |
| msgflow.service.CronService | Get messages on a regular basis | o  | | |
| msgflow.service.WebapiService | Get and respond a message as Web API  | o | o |  |
| msgflow.service.SlackService | Get mentions and respond in the same thread as a original message. This Service also supports to post a specified channel. | o | o | o |
| msgflow.service.TwitterSampleStreamService | Retrieve tweets via [Twitter sampled stream v2](https://developer.twitter.com/en/docs/twitter-api/tweets/sampled-stream/api-reference/get-tweets-sample-stream) | o | | | Background |

o: available, blank: unavailable