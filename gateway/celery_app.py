# ==========================================
# gateway/celery_app.py
# ==========================================
from celery import Celery
# Assuming common config is importable, otherwise define BROKER_URL etc. here
from common.celery_config import BROKER_URL, RESULT_BACKEND

# Celery app instance purely for sending tasks from the gateway
# No task implementations are needed here.
gateway_producer = Celery(
    'gateway_producer', # Name for identification, doesn't define task namespace
    broker=BROKER_URL,
    backend=RESULT_BACKEND, # Gateway might want results sometimes
    include=[] # Explicitly state no task modules included
)

gateway_producer.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

