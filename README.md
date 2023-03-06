# yobagpt_bot

[![\[Telegram\] aiogram live](https://img.shields.io/badge/telegram-aiogram-blue.svg?style=flat-square)](https://t.me/aiogram_live)
[![Supported python versions](https://img.shields.io/pypi/pyversions/aiogram.svg?style=flat-square)](https://pypi.python.org/pypi/aiogram)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-6.5-blue.svg?style=flat-square&logo=telegram)](https://core.telegram.org/bots/api)
[![MIT License](https://img.shields.io/pypi/l/aiogram.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Simple `ChatGPT` and `aiogram` integration.

## Config and environments variable

Config based on `.env` creation or set env-variables as you like (example: [.env.default](.env.default))

### `LOG_LEVEL`

By default: `logging.INFO`

### `TELEGRAM_API_KEY`

- Find [BotFather](https://t.me/BotFather) account
- Create a new bot
- Generate API token and put it to config

### `CHAT_ACCESS_TOKEN`

- It is valid for 4 weeks
- Can be found if you log in to `https://chat.openai.com/` and then go to `https://chat.openai.com/api/auth/session`
- Put `accessToken` to config

### `OPEANAI_API_KEY`

- Log in to `https://platform.openai.com/account/api-keys`
- Create a new secret key
- Put a new secret key to config

## How to run

### Without Docker:

- Make virtual environment
- Install package requirements
- Create `.env` or set env-variables as you like (example: [.env.default](.env.default))
- Run it! :)

### With Docker

- Create `.env` or set env-variables as you like (example: [.env.default](.env.default)
  and see [docker-compose.yml](docker-compose.yml))
- Run it! :)

## Development tools

### Bandit tool

[Bandit](https://github.com/PyCQA/bandit) is a tool designed to find common security issues in Python code. To do this
Bandit processes each file, builds an AST from it, and runs appropriate plugins against the AST nodes. Once Bandit has
finished scanning all the files it generates a report.

```shell
bandit -r .
```

### flake8

[flake8](https://github.com/PyCQA/flake8) is a python tool that glues together pycodestyle, pyflakes, mccabe, and
third-party plugins to check the style and quality of some python code.

```shell
flake8 .
```

### Logs format

```shell
      INFO | 2023-03-06 11:19:58,649 |                        aiogram |          executor.py |    362 | Bot: <bot_name_here> [@<bot_username_here>]
   WARNING | 2023-03-06 11:19:58,830 |                        aiogram |          executor.py |    358 | Updates were skipped successfully.
      INFO | 2023-03-06 11:19:58,839 |  aiogram.dispatcher.dispatcher |        dispatcher.py |    358 | Start polling.
```
