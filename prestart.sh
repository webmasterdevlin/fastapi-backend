#! /usr/bin/env bash

# Let the DB start
python src/app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python src/app/initial_data.py
