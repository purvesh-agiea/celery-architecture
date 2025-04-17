from order_service.celery_app import app
from common.celery_config import NOTIFICATION_QUEUE
import time
import random


@app.task(bind=True)
def process_order_task(self, order_id: str, order_details: dict):
    """
    Processes the received order details.
    Simulates DB operations and triggers notification task.
    """
    worker_hostname = self.request.hostname or 'unknown_worker'
    print(f"[{worker_hostname} - OrderService]: Processing order {order_id} for {order_details['customer_email']}")

    try:
        print(f"[{worker_hostname} - OrderService]: Validating order {order_id}...")
        time.sleep(random.uniform(1, 3))
        print(f"[{worker_hostname} - OrderService]: Saving order {order_id} to database...")
        time.sleep(random.uniform(0.5, 1.5))
        print(f"[{worker_hostname} - OrderService]: Updating inventory for item {order_details['item_id']}...")
        time.sleep(random.uniform(0.5, 1))

        notification_task_name = 'notification_service.tasks.send_order_confirmation_task'
        print(f"[{worker_hostname} - OrderService]: Order {order_id} processed. Queueing notification task.")

        app.send_task(
            notification_task_name,
            args=[order_id, order_details['customer_email']],
            queue=NOTIFICATION_QUEUE  # Send to the notification service's queue
        )

        print(
            f"[{worker_hostname} - OrderService]: Notification task for order {order_id} sent to queue '{NOTIFICATION_QUEUE}'")
        return f"Order {order_id} processed successfully."

    except Exception as e:
        print(f"[{worker_hostname} - OrderService]: FAILED processing order {order_id}. Reason: {e}")
        raise
