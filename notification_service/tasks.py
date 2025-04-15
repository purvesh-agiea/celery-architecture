# ==========================================
# notification_service/tasks.py
# ==========================================
# Adjust path if needed when running worker
# import os
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from notification_service.celery_app import app
import time
import random

# This task will be named 'notification_service.tasks.send_order_confirmation_task'
@app.task(bind=True)
def send_order_confirmation_task(self, order_id: str, customer_email: str):
    """
    Simulates sending an order confirmation email/SMS.
    """
    worker_hostname = self.request.hostname or 'unknown_worker'
    print(f"[{worker_hostname} - NotificationService]: Preparing confirmation for order {order_id} to {customer_email}")

    try:
        # Simulate connecting to email service and sending
        print(f"[{worker_hostname} - NotificationService]: Connecting to email provider...")
        time.sleep(random.uniform(0.5, 1))
        print(f"[{worker_hostname} - NotificationService]: Sending email for order {order_id} to {customer_email}...")
        time.sleep(random.uniform(1, 2)) # Simulate network latency

        # Simulate success
        print(f"[{worker_hostname} - NotificationService]: Successfully sent confirmation for order {order_id}")
        return f"Confirmation for {order_id} sent."

    except Exception as e:
        print(f"[{worker_hostname} - NotificationService]: FAILED sending confirmation for order {order_id}. Reason: {e}")
        # Add retry logic if appropriate for notifications
        # raise self.retry(exc=e, countdown=60, max_retries=5)
        raise
