# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Introduce Messenger to handle a context in conversations https://github.com/colorfulscoop/msgflow/pull/27

### Removed

- DialogMemory because This feature is available via context

## [v0.6.0] - 2021-01-11

### Added

- Implement clear method in DialogMemory https://github.com/colorfulscoop/msgflow/pull/19
- Source property to Message object https://github.com/colorfulscoop/msgflow/pull/22
- [WebApiService] data attribute in the request https://github.com/colorfulscoop/msgflow/pull/23
- [WebApiService] endpoint option in config https://github.com/colorfulscoop/msgflow/pull/23

### Changed

- Update TwitterSampleStreamService to adopt Twitter API v2 https://github.com/colorfulscoop/msgflow/pull/21

### Removed

- Temporarily disable TwitterMentionsTimeline service because it does not work with Twitter API v2 https://github.com/colorfulscoop/msgflow/pull/21

## [v0.5.0] - 2021-01-09

### Added

- CronService https://github.com/colorfulscoop/msgflow/pull/16

### Changed

- `conversation_id` to `dialog_id` https://github.com/colorfulscoop/msgflow/pull/17

## [v0.4.0] - 2021-01-02

### Changed

- Service interface to add `from_config` for initializing the object from config dictionary https://github.com/colorfulscoop/msgflow/pull/14

## [v0.3.0] - 2020-12-29

### Added

- CI for github actions https://github.com/colorfulscoop/msgflow/pull/6
- Code style check https://github.com/colorfulscoop/msgflow/pull/7
- Protocol to define interface https://github.com/colorfulscoop/msgflow/pull/8
- ContextMemory to keep track of conversations https://github.com/colorfulscoop/msgflow/pull/9
- Queue based handler execution in background https://github.com/colorfulscoop/msgflow/pull/12

### Changed

- Add `conversation_id` property to Message protocol https://github.com/colorfulscoop/msgflow/pull/10

## [0.2.1] - 2020-09-09

### Added

- TwitterMentionsTimelineService

### Fixed

- Slack service which process to deal with messages without any suspending time
- Twitter mention timeline service to add exception statement to connect to Twitter https://github.com/noriyukipy/msgflow/pull/4

## [0.2.0] - 2020-08-17

### Changed

- Package name to msgFlow

## [0.1.1] - 2020-07-25

### Fixed

- Slack response bug which sends system text to user as a reply
- Retry RTM Slack connection when connection is broken

## [0.1.0] - 2020-07-18

### Added

- Custom application architecture
- New services: CliService, SlackService and TwitterSampleStreamService
- YAML parser to inject environment variables
