# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.3.0] - 2020-12-29

### Added

- Add CI for github actions https://github.com/colorfulscoop/msgflow/pull/6
- Add code style check https://github.com/colorfulscoop/msgflow/pull/7
- Add protocol to define interface https://github.com/colorfulscoop/msgflow/pull/8
- Add ContextMemory to keep track of conversations https://github.com/colorfulscoop/msgflow/pull/9
- Add queue based handler execution in background https://github.com/colorfulscoop/msgflow/pull/12

### Changed

- Add `conversation_id` property to Message protocol https://github.com/colorfulscoop/msgflow/pull/10

## [0.2.1] - 2020-09-09

### Added

- TwitterMentionsTimelineService

### Fixed

- Fix slack service which process to deal with messages without any suspending time
- Fix Twitter mention timeline service to add exception statement to connect to Twitter https://github.com/noriyukipy/msgflow/pull/4

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
