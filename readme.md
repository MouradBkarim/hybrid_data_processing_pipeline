## 📊 Real-Time & Batch Data Pipeline — Home Assessment

### 🧭 Overview

This project demonstrates a hybrid **real-time + batch data processing pipeline** using modern data engineering tools and Docker-based orchestration. It includes:

- **Real-time ingestion** via RabbitMQ (producer/consumer pattern)
- **Batch processing** with Spark + Delta Lake triggered via Airflow or Jupyter
- **Data lake emulation** via S3Mock (bronze, silver, gold zones)
- **Monitoring/analysis** via Streamlit dashboard
- **Workflow automation** using Airflow (ETL orchestration & notebook triggering)

This end-to-end pipeline covers ingestion, storage, transformation, and visualization—showcasing data architecture, engineering, and DevOps capabilities.

---

### 🏗️ Architecture

```plaintext
                        +------------------+
                        |  RabbitMQ        |
                        | (Producer/Queue) |
                        +--------+---------+
                                 |
                                 v
                         +-------+--------+
                         | RabbitMQ       |
                         | Consumer       |
                         | (Writes Bronze |
                         |  S3 layer)     |
                         +-------+--------+
                                 |
       ┌─────────────Batch Notebook / Airflow──────────────┐
       ↓                                                   ↓
+---------------+        +----------------+        +------------------+
|  Bronze (S3)  | -----> |  Silver (S3)   | -----> |  Gold (S3)       |
+---------------+        +----------------+        +------------------+
     Raw data           Cleaned/formatted        Aggregated results
     (Json & delta)                (delta)                   (delta)

        ↑
        |
+---------------+
| Postgres      |
| (source data) |
+---------------+

        ↓
+----------------+
|  Streamlit     |
|  Dashboard     |
+----------------+

        ↓
+----------------+
|  Jupyter       |
|  Notebook UI   |
+----------------+

```

---

### ⚙️ Project Structure

```
├── airflow/                 → Airflow DAGs and Docker build
├── jupyter/                 → Jupyter notebooks and Dockerfile
├── postgres-producer/       → Ingests static data into Postgres
├── rabbitmq/producer/       → Real-time event producer
├── rabbitmq/consumer/       → Consumer writing to S3 (bronze)
├── dashboard/               → Streamlit dashboard
├── local-s3/                → Auto created local folder which is mounted as S3Mock
├── docker-compose.yml       → Multi-service orchestration
├── start_env.sh             → Sets up the environment
├── run_postgres_producer.sh → Loads Postgres sample data
├── run_realtime_pipeline.sh → Starts RabbitMQ producer/consumer
```

---

### 🚀 Run Instructions

#### 1. Start full environment

```bash
./start_env.sh
```

> 🧼 This cleans and rebuilds everything (Airflow, RabbitMQ, Postgres, Jupyter, Streamlit, S3Mock)

#### 2. Load batch source data into Postgres

```bash
./run_postgres_producer.sh
```

#### 3. Run real-time producer and consumer

```bash
./run_realtime_pipeline.sh
```

#### 4. Run batch pipeline manually

- Option A: Trigger the Airflow DAG: `run_postgres_etl_notebook`:[http://localhost:8080/](http://localhost:8080/)

  Username/Password: admin/admin

- Option B: Open Jupyter: [http://localhost:8888/](http://localhost:8888/)

  Token: `test-token`

  Then run the notebook: `batch.ipynb`

#### 5. Run real time pipeline manually

- Open Jupyter: [http://localhost:8888/](http://localhost:8888/)

  Token: `test-token`

  Then run the notebook: `bronze_silver_preprocessing.ipynb`, and `gold_aggregate_dashboard.ipynb`

#### 6. Visualize results

- Open Streamlit dashboard: [http://localhost:8501/](http://localhost:8501/)
- In the home page, you would see User Activity per Event Type per Day in real time

---

### 🔧 Notes

- S3 paths: `/mnt/s3mock/bronze`, `/mnt/s3mock/silver`, `/mnt/s3mock/gold`
- Delta tables are written via Spark with `delta-spark==2.4.0`
- Airflow DAGs are stored in `./airflow/dags`
- The Jupyter container runs on ports `8888` (token access) and `9999` (optional extensions)
