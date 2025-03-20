#!/bin/bash

# Check the CELERY_MODE environment variable
if [ "$CELERY_MODE" = "worker" ]; then
    echo "Starting Celery Worker..."
    celery -A app.celery_app worker \
        --loglevel=info \
        --hostname=worker@%h \
        --concurrency=${CONCURRENCY}
elif [ "$CELERY_MODE" = "beat" ]; then
    echo "Starting Celery Beat..."
    celery -A app.celery_app beat \
        --loglevel=info \
        --max-interval=${MAX_INTERVAL}
else
    echo "Error: Invalid CELERY_MODE. Set it to 'worker' or 'beat'."
    exit 1
fi
