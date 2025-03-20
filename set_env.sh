# CONCURRENCY = CPU cores * 2
# export CELERY_MODE="" (worker or beat)
export CONCURRENCY="3"
export MAX_INTERVAL=60
export SCHEDULER_SYNC_EVERY=30

export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export REDIS_DB="0"

export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_USER="postgres"
export POSTGRES_PASSWORD=""
export POSTGRES_DB="test"

export CELERY_TIMEZONE="Asia/kolkata"
export CELERY_ENABLE_UTC="False"

export LOG_LEVEL="INFO"
