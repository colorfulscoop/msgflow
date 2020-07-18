# SmileChat

SmileChat is a simple chatbot framework written in Python for simple configuration, customization and connection with several services.

## Installation

```sh
$ pip install git+https://github.com/noriyukipy/pybot
```

## Documents

Documents are provided in https://smilingchat.net/smilechat/.
You can start using SmileChat with [Getting Started](https://smilingchat.net/smilechat/getting_started/) .

## Building Documents

The document is provided by [MkDocs](https://www.mkdocs.org/) and published by [gh-pages](https://www.npmjs.com/package/gh-pages).

First, build your document to convert markdown files to HTML files.

```sh
$ bash docs_builder.sh build
```

Then built files are placed in `docs/site` .

After checking the content, run `gh-pages` to commit on gh-pages and push to GitHub.

```sh
GIT_USER="Your Name <email@example.com>" bash docs_builder.sh publish
```
