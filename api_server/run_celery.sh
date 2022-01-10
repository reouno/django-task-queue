#!/bin/sh

sleep 10

celery -A api_server worker -l info