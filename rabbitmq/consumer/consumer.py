import pika
import json
import os
import time
from datetime import datetime

QUEUE_NAME = 'test-queue-events'
OUTPUT_DIR = '/data/bronze/realtime/events'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def connect_to_rabbitmq():
    retries = 5
    for i in range(retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    credentials=pika.PlainCredentials('admin', 'secret')
                )
            )
            return connection
        except Exception as e:
            print(f"RabbitMQ not ready, retrying in 5s... ({i+1}/{retries})")
            time.sleep(5)
    raise Exception("Failed to connect to RabbitMQ after multiple attempts.")

def callback(ch, method, properties, body):
    try:
        event = json.loads(body)
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
        filename = f"{OUTPUT_DIR}/event_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(event, f)
        print(f"Saved event to {filename}")
    except Exception as e:
        print(f"Failed to process message: {e}")

connection = connect_to_rabbitmq()
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME, durable=True)

print("Listening for events...")
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
