#!/usr/bin/env bash
# This script runs on every deploy, on Render's servers (not your PC).
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
