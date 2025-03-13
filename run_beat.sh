#!/bin/bash
celery -A app.celery_app beat \
    --loglevel=info \
    --max-interval=60