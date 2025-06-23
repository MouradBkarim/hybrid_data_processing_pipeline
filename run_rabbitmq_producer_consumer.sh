#!/bin/bash
set -e

echo "Starting RabbitMQ producer and consumer..."

docker compose up -d producer consumer

echo "Producer and consumer started."
