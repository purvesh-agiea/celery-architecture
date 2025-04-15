# ==========================================
# gateway/main.py
# ==========================================
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import os
import sys

# Adjust path to import from sibling directories if running directly
# This might be needed depending on how you run the gateway
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from gateway.celery_app import gateway_producer
from common.celery_config import ORDER_PROCESSING_QUEUE

app = FastAPI(title="E-commerce API Gateway")

class OrderPayload(BaseModel):
    customer_email: str
    item_id: str
    quantity: int

@app.post("/orders", status_code=202) # 202 Accepted: Request taken, processing started
async def place_order(order: OrderPayload):
    """
    Accepts an order and queues it for processing.
    """
    order_id = str(uuid.uuid4())
    print(f"Gateway: Received order {order_id} for item {order.item_id}")

    # Define the full name of the task as implemented in the Order Service
    order_task_name = 'order_service.tasks.process_order_task'

    try:
        # Send the task to the specific queue for the Order Service
        gateway_producer.send_task(
            order_task_name,
            args=[order_id, order.dict()], # Pass order details
            kwargs={},
            queue=ORDER_PROCESSING_QUEUE # Route to the order processing queue
        )
        print(f"Gateway: Task for order {order_id} sent to queue '{ORDER_PROCESSING_QUEUE}'")
        return {"message": "Order received and queued for processing.", "order_id": order_id}
    except Exception as e:
        # Handle potential connection errors with the broker
        print(f"Gateway: ERROR - Could not queue order {order_id}. Reason: {e}")
        raise HTTPException(status_code=503, detail="Order processing service unavailable.")

# To run (requires uvicorn and fastapi):
# Ensure current directory is the parent of 'gateway', 'order_service', etc.
# PYTHONPATH=. uvicorn gateway.main:app --reload --port 8000
