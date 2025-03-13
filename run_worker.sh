#!/bin/bash
celery -A app.celery_app worker \
    --loglevel=info \
    --hostname=worker@%h \
    --autoscale=3,1