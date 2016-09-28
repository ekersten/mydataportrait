#!/usr/bin/env bash
echo "Updating from Git"
git pull
echo "Activating virtualenv"
source /home/development/.virtualenvs/dataportrait/bin/activate
echo "Installing requirements"
cd /home/development/projects/dataportrait/dataportrait
pip install -r requirements.txt
echo "Updating DB Schema"
python manage.py migrate
echo "Collecting static assets"
python manage.py collectstatic --no-input
echo "Deactivating virtualenv"
deactivate
echo "Deploy complete!"
