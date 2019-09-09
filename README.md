# Small Improvements - 360 Feedback

> Sharing the 360 feedback to your reviewee will not be the same again. This script will retrieve the 360 feedback data from Small Improvements.

[![CircleCI](https://circleci.com/gh/prontotools/si360feedback.svg?style=svg)](https://circleci.com/gh/prontotools/si360feedback)

## Installation

1. Install the package manager for macOS `brew` from [Homebrew](https://brew.sh/) first.
1. Install `pipenv`, run
    ```sh
    brew install pipenv
    ```
1. Install the dependencies used in this project, run
    ```sh
    pipenv install
    ```
1. Copy `env.example` to `.env` and put your credentials.

## Usage Example

```sh
pipenv run python program.py > your_reviewee.html
```

## Development Setup

```sh
pipenv install --dev
pipenv run flake8
pipenv run pytest
```

## Contributing

1. Fork it (<https://github.com/prontotools/si360feedback/fork>)
1. Create your feature branch (`git checkout -b feature/fooBar`)
1. Commit your changes (`git commit -am 'Add some fooBar'`)
1. Push to the branch (`git push origin feature/fooBar`)
1. Create a new Pull Request
