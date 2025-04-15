# ==========================================
# common/celery_config.py
# ==========================================
# Using RabbitMQ here, replace with your broker URL (e.g., Redis) if needed
BROKER_URL = 'redis://localhost:6379/1'
RESULT_BACKEND = 'redis://localhost:6379/1' # Optional, but good for tracking

# Define queue names clearly
ORDER_PROCESSING_QUEUE = 'order_processing'
NOTIFICATION_QUEUE = 'notifications'