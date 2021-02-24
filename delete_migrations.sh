#!/usr/bin/env sh

mv esnpolimi_mgmt/migrations/0004_createsuperuser.py .
mv esnpolimi_mgmt/migrations/0003_createaccounts.py .

find . -path "**/migrations/*.py" -not -path "**/contrib/sites/*" -not -name "__init__.py" -delete
find . -path "**/migrations/__pycache__/*" -delete
find . -path "**/migrations/*.pyc" -delete

find . -path "**/__pycache__/*" -delete

python manage.py makemigrations

mv esnpolimi_mgmt/migrations/0002_*.py esnpolimi_mgmt/migrations/0002_initial2.py
mv 0004_createsuperuser.py esnpolimi_mgmt/migrations/
mv 0003_createaccounts.py esnpolimi_mgmt/migrations/
