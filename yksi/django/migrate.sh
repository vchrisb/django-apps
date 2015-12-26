#!/bin/sh
echo "------ Create database tables ------"
python manage.py migrate --noinput

echo "------ starting gunicorn  ------"
gunicorn yksi.wsgi --workers 2
