import pika
import json
import time
import random
from datetime import datetime

QUEUE_NAME = 'test-queue-events'
EVENT_TYPES = ["opened_app", "browsed_merchants", "checked_in"]

def generate_event():
    return {
        "user_id": f"user_{random.randint(1, 100)}",
        "event_type": random.choice(EVENT_TYPES),
        "timestamp": datetime.utcnow().isoformat(),
        "location": {
            "lat": round(random.uniform(48.1, 54.9), 5),
            "lon": round(random.uniform(8.4, 13.1), 5)
        }
    }

def connect_to_rabbitmq():
    retries = 5
    for i in range(retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='rabbitmq', credentials=pika.PlainCredentials('admin', 'secret'))
            )
            return connection
        except Exception as e:
            print(f"RabbitMQ not ready, retrying in 5s... ({i+1}/{retries})")
            time.sleep(5)
    raise Exception("Failed to connect to RabbitMQ after multiple attempts.")

connection = connect_to_rabbitmq()
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=True)

print(" Start producing events to RabbitMQ...")

while True:
    event = generate_event()
    message = json.dumps(event)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f"Sent: {message}")
    time.sleep(2)
