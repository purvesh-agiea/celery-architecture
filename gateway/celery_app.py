from celery import Celery
from common.celery_config import BROKER_URL, RESULT_BACKEND

gateway_producer = Celery(
    'gateway_producer',
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=[]
)

gateway_producer.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
