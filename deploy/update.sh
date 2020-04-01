#!/usr/bin/env bash

set -e

PROJECT_BASE_PATH='/usr/local/apps/torshavn_api'

git pull
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput
$PROJECT_BASE_PATH/requirements.txt
supervisorctl restart torshavn_api

echo "DONE! :)"
