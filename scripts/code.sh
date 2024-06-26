#!/bin/sh
poetry run black ditto
poetry run isort ditto
poetry run yapf -i -r ditto