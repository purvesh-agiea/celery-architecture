from celery import Celery
from common.celery_config import BROKER_URL, RESULT_BACKEND, ORDER_PROCESSING_QUEUE, NOTIFICATION_QUEUE

app = Celery(
    'order_service.tasks',
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=['order_service.tasks']
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_queues={
        ORDER_PROCESSING_QUEUE: {
            'exchange': ORDER_PROCESSING_QUEUE,
            'routing_key': ORDER_PROCESSING_QUEUE,
        },
        NOTIFICATION_QUEUE: {
            'exchange': NOTIFICATION_QUEUE,
            'routing_key': NOTIFICATION_QUEUE,
        }
    },
)
