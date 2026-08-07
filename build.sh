#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get(chr(39)DJANGO_SUPERUSER_USERNAMEchr(39))
email = os.environ.get(chr(39)DJANGO_SUPERUSER_EMAILchr(39))
password = os.environ.get(chr(39)DJANGO_SUPERUSER_PASSWORDchr(39))
if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(chr(39)Superuser created.chr(39))
else:
    print(chr(39)Superuser already exists or env vars missing, skipping.chr(39))
"
