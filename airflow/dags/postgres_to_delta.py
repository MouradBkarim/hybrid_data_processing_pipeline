import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def trigger_notebook():
    res = requests.post("http://notebook:9999/run-notebook")
    if res.status_code != 200:
        raise Exception(f"!!!Notebook failed: {res.text}")

with DAG(
    dag_id="run_postgres_etl_notebook",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    run = PythonOperator(
        task_id="trigger_jupyter_notebook",
        python_callable=trigger_notebook
    )
