# ==========================================
# notification_service/__init__.py
# ==========================================
# (This file can be empty)


# ==========================================
# notification_service/celery_app.py
# ==========================================
from celery import Celery
# Assuming common config is importable
from common.celery_config import BROKER_URL, RESULT_BACKEND, NOTIFICATION_QUEUE

# This Celery app instance is for the Notification Service worker
app = Celery(
    'notification_service.tasks', # Namespace for tasks in this service
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=['notification_service.tasks'] # Module(s) containing tasks
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_queues={
        NOTIFICATION_QUEUE: {
            'exchange': NOTIFICATION_QUEUE,
            'routing_key': NOTIFICATION_QUEUE,
        }
    },
)