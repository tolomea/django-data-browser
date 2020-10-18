#!/bin/bash
set -ex

rm -Rf dist build
python -m pip install -U pip
python -m pip install --upgrade setuptools wheel twine check-manifest
check-manifest -v
python setup.py sdist bdist_wheel
twine check dist/*
