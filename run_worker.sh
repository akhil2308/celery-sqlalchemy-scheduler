#!/bin/bash
celery -A app.celery_app worker \
    --loglevel=info \
    --hostname=worker@%h \
    --concurrency=${CONCURRENCY}
