from notification_service.celery_app import app
import time
import random

@app.task(bind=True)
def send_order_confirmation_task(self, order_id: str, customer_email: str):
    """
    Simulates sending an order confirmation email/SMS.
    """
    worker_hostname = self.request.hostname or 'unknown_worker'
    print(f"[{worker_hostname} - NotificationService]: Preparing confirmation for order {order_id} to {customer_email}")

    try:
        print(f"[{worker_hostname} - NotificationService]: Connecting to email provider...")
        time.sleep(random.uniform(0.5, 1))
        print(f"[{worker_hostname} - NotificationService]: Sending email for order {order_id} to {customer_email}...")
        time.sleep(random.uniform(1, 2))

        # Simulate success
        print(f"[{worker_hostname} - NotificationService]: Successfully sent confirmation for order {order_id}")
        return f"Confirmation for {order_id} sent."

    except Exception as e:
        print(f"[{worker_hostname} - NotificationService]: FAILED sending confirmation for order {order_id}. Reason: {e}")
        raise
