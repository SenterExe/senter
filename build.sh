#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install remind==0.17.0
poetry install
pip install --upgrade pip
pip install --force-reinstall -U setuptools
python manage.py collectstatic --no-input
python manage.py migrate