#!/bin/bash
pip install -r requirements.txt
cd familog
python manage.py collectstatic --noinput
