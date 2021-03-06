#!/bin/sh
echo "------ Create database tables ------"
python manage.py migrate --noinput

echo "------ create default admin user ------"
python manage.py shell < superuser.py

echo "------ starting gunicorn  ------"
gunicorn yksi.wsgi --workers 2
