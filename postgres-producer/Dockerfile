FROM python:3.11-slim

WORKDIR /app

RUN pip install psycopg2-binary

COPY generate_postgres_data.py .

CMD ["python", "generate_postgres_data.py"]
