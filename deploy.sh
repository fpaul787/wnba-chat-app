#!/bin/sh
set -e     
source env/bin/activate
sudo pip3 install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
rm -r static
python manage.py collectstatic --noinput
sudo service apache2 restart
