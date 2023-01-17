<div align="center">

# Virus Total Telegram bot

A telegram bot for quick checks on the security of files, URLs and other resources.

[Contributing Guidelines](./CONTRIBUTING.md) · [Request a Feature](https://github.com/clarriu97/virus-total-telegram-bot/-/issues/new?issuable_template=Feature) · [Report a Bug](https://github.com/clarriu97/virus-total-telegram-bot/-/issues/new?issuable_template=Bug)

</div>

## Usage

You can install this package using [pip](https://pip.pypa.io/en/stable/):

```
$ pip install virus_total_telegram_bot
```

You can now import this module on your Python project:

```python
import virus_total_telegram_bot
```

## Development

To start developing this project, clone this repo and do:

```
$ make env-create
```

This will create a virtual environment with all the needed dependencies (using [tox](https://tox.readthedocs.io/en/latest/)). You can activate this environment with:

```
$ source ./.tox/virus_total_telegram_bot/bin/activate
```

Then, you can run `make help` to learn more about the different tasks you can perform on this project using [make](https://www.gnu.org/software/make/).

## License

[Copyright](./LICENSE)