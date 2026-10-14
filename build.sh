#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files for production
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Seed initial multi-class demo data
python reset_and_seed.py
