from celery import Celery
from common.celery_config import BROKER_URL, RESULT_BACKEND, NOTIFICATION_QUEUE

app = Celery(
    'notification_service.tasks',
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=['notification_service.tasks']
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
