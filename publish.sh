#!/usr/bin/env bash
pip install wheel
set -e

rm -rf dist
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
