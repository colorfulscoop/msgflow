# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- Slack response bug which sends system text to user as a reply
- Retry RTM Slack connection when connection is broken

## [0.1.0] - 2020-07-18
### Added
- Custom application architecture
- New services: CliService, SlackService and TwitterSampleStreamService
- YAML parser to inject environment variables
