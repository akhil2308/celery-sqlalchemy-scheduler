from app.celery_app import celery
import logging

logger = logging.getLogger(__name__)

@celery.task(name="send_email")
def send_email(args):
    logger.info(f"Sending email: {args}")
    # Email sending logic here