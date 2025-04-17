from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

from gateway.celery_app import gateway_producer
from common.celery_config import ORDER_PROCESSING_QUEUE

app = FastAPI(title="E-commerce API Gateway")


class OrderPayload(BaseModel):
    customer_email: str
    item_id: str
    quantity: int


@app.post("/orders", status_code=202)
async def place_order(order: OrderPayload):
    """
    Accepts an order and queues it for processing.
    """
    order_id = str(uuid.uuid4())
    print(f"Gateway: Received order {order_id} for item {order.item_id}")

    order_task_name = 'order_service.tasks.process_order_task'

    try:
        gateway_producer.send_task(
            order_task_name,
            args=[order_id, order.dict()],
            kwargs={},
            queue=ORDER_PROCESSING_QUEUE
        )
        print(f"Gateway: Task for order {order_id} sent to queue '{ORDER_PROCESSING_QUEUE}'")
        return {"message": "Order received and queued for processing.", "order_id": order_id}
    except Exception as e:
        print(f"Gateway: ERROR - Could not queue order {order_id}. Reason: {e}")
        raise HTTPException(status_code=503, detail="Order processing service unavailable.")
