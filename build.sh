#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip

poetry install
pip install --upgrade pip
pip install --force-reinstall -U setuptools
python manage.py collectstatic --no-input --clear
python manage.py migrate