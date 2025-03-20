from celery import Celery
from .config import Config
import logging
logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)

def create_celery_app():
    app = Celery(__name__)
    app.conf.update(
        broker_url=Config.CELERY_BROKER_URL,
        result_backend=Config.CELERY_RESULT_BACKEND,
        timezone=Config.CELERY_TIMEZONE,
        # enable_utc=Config.CELERY_ENABLE_UTC,
        beat_scheduler="app.scheduler.SQLAlchemyScheduler",
        imports=[
            "app.tasks.email_tasks",
        ]
    )
    return app

celery = create_celery_app()
