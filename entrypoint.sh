#!/bin/bash

echo "Применяем миграции..."
python manage.py migrate

echo "Собираем статику"
python manage.py collectstatic

echo "Starting the main process..."
exec /usr/bin/supervisord