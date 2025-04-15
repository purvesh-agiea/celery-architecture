# ==========================================
# order_service/celery_app.py
# ==========================================
from celery import Celery
# Assuming common config is importable
from common.celery_config import BROKER_URL, RESULT_BACKEND, ORDER_PROCESSING_QUEUE, NOTIFICATION_QUEUE

# This Celery app instance is for the Order Service worker
# The name 'order_service.tasks' is important as it forms the prefix for task names
app = Celery(
    'order_service.tasks', # Namespace for tasks defined within this service
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=['order_service.tasks'] # Module(s) containing task definitions
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # Define the queues this worker might interact with
    task_queues={
        ORDER_PROCESSING_QUEUE: {
            'exchange': ORDER_PROCESSING_QUEUE,
            'routing_key': ORDER_PROCESSING_QUEUE,
        },
         # It also needs to know about the notification queue to send tasks TO it
        NOTIFICATION_QUEUE: {
            'exchange': NOTIFICATION_QUEUE,
            'routing_key': NOTIFICATION_QUEUE,
        }
    },
)