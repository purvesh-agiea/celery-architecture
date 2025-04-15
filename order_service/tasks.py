# ==========================================
# order_service/tasks.py
# ==========================================
# Adjust path if needed when running worker
# import os
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from order_service.celery_app import app
from common.celery_config import NOTIFICATION_QUEUE # Need queue name to send next task
import time
import random

# This task will be named 'order_service.tasks.process_order_task'
@app.task(bind=True)
def process_order_task(self, order_id: str, order_details: dict):
    """
    Processes the received order details.
    Simulates DB operations and triggers notification task.
    """
    worker_hostname = self.request.hostname or 'unknown_worker'
    print(f"[{worker_hostname} - OrderService]: Processing order {order_id} for {order_details['customer_email']}")

    try:
        # Simulate database save / validation / inventory check
        print(f"[{worker_hostname} - OrderService]: Validating order {order_id}...")
        time.sleep(random.uniform(1, 3))
        print(f"[{worker_hostname} - OrderService]: Saving order {order_id} to database...")
        time.sleep(random.uniform(0.5, 1.5))
        print(f"[{worker_hostname} - OrderService]: Updating inventory for item {order_details['item_id']}...")
        time.sleep(random.uniform(0.5, 1))

        # Order processed successfully, now trigger notification
        notification_task_name = 'notification_service.tasks.send_order_confirmation_task'
        print(f"[{worker_hostname} - OrderService]: Order {order_id} processed. Queueing notification task.")

        # Use the same Celery app instance ('app' from order_service.celery_app)
        # to send the *next* task in the chain.
        app.send_task(
            notification_task_name,
            args=[order_id, order_details['customer_email']],
            queue=NOTIFICATION_QUEUE # Send to the notification service's queue
        )

        print(f"[{worker_hostname} - OrderService]: Notification task for order {order_id} sent to queue '{NOTIFICATION_QUEUE}'")
        return f"Order {order_id} processed successfully."

    except Exception as e:
        print(f"[{worker_hostname} - OrderService]: FAILED processing order {order_id}. Reason: {e}")
        # Implement retry logic or error handling (e.g., move to dead-letter queue)
        # For simplicity, we just re-raise here, Celery will mark task as failed.
        raise