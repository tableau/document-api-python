#!/usr/bin/env bash

set -e

rm -rf dist
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
