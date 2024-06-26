#!/usr/bin/env sh

poetry run python -m pytest --cov=ditto --cov-report term-missing tests
