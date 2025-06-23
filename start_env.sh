#!/bin/bash
set -e

echo "Cleaning up existing Docker containers, volumes, and networks..."
docker compose down --volumes --remove-orphans

echo "Removing dangling Docker images and containers..."
docker system prune -af --volumes

echo "Building all services..."
docker compose build

echo "Starting environment: RabbitMQ, Jupyter, Airflow, Postgres, S3Mock, Streamlit..."
docker compose up -d rabbitmq postgres s3mock notebook airflow airflow-scheduler streamlit_app

echo "Waiting for Postgres to become healthy..."
until [ "$(docker inspect -f '{{.State.Health.Status}}' hybrid_data_processing_pipeline-postgres-1)" == "healthy" ]; do
  sleep 2
done

echo "Environment is up!"
docker compose ps
