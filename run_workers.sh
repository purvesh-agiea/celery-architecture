# ==========================================
# run_workers.sh
# ==========================================
#!/bin/bash

echo "Starting E-commerce Celery Workers..."

# Make sure RabbitMQ & Redis (if used for backend) are running!
# Ensure you run this script from the directory containing the service folders
# (e.g., ecommerce_celery/)
# Set PYTHONPATH to include the current directory so imports work
export PYTHONPATH=.

# Start Order Service Worker
# - Listens ONLY to 'order_processing' queue
# - Allows up to 5 concurrent tasks (-c 5)
# - Fetches only 1 task ahead per worker process (--prefetch-multiplier=1)
echo "Starting Order Service Worker (Concurrency=5, Queue=order_processing)..."
celery -A order_service.celery_app worker -l info \
       -Q order_processing \
       -c 5 \
       --prefetch-multiplier=1 \
       --hostname=order_worker@%h & # Run in background
ORDER_PID=$!
echo "Order Service Worker PID: $ORDER_PID"
sleep 2 # Give worker time to start before starting the next

# Start Notification Service Worker
# - Listens ONLY to 'notifications' queue
# - Allows up to 10 concurrent tasks (-c 10)
# - Fetches only 1 task ahead per worker process (--prefetch-multiplier=1)
echo "Starting Notification Service Worker (Concurrency=10, Queue=notifications)..."
celery -A notification_service.celery_app worker -l info \
       -Q notifications \
       -c 10 \
       --prefetch-multiplier=1 \
       --hostname=notify_worker@%h & # Run in background
NOTIFY_PID=$!
echo "Notification Service Worker PID: $NOTIFY_PID"


echo "Workers started. Press Ctrl+C in this terminal to stop them."

# Basic mechanism to keep script running and allow stopping workers
# When Ctrl+C is pressed, the trap catches the SIGINT signal and kills the background PIDs
trap "echo 'Stopping workers...'; kill $ORDER_PID $NOTIFY_PID 2>/dev/null; exit" SIGINT SIGTERM

# Wait indefinitely until a signal (like SIGINT from Ctrl+C) is received
wait