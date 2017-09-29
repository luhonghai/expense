#!/bin/bash
python /usr/local/expense/manage.py migrate
cd /usr/local/expense/
python /usr/local/expense/manage.py runserver --noreload 0.0.0.0:8000