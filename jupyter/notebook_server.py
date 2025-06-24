from flask import Flask, jsonify
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
import subprocess

app = Flask(__name__)

def get_spark():
    builder = SparkSession.builder.appName("NotebookQueryAPI") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    return configure_spark_with_delta_pip(builder).getOrCreate()

spark = get_spark()

@app.route('/run-notebook', methods=['POST'])
def run():
    result = subprocess.run(
        ["papermill", "work/batch.ipynb", "work/output_batch.ipynb"],
        capture_output=True
    )
    return result.stdout.decode() + "\n\n" + result.stderr.decode(), 200

@app.route("/api/gold-aggregates", methods=["GET"])
def get_gold_data():
    df = spark.read.format("delta").load("/mnt/s3mock/gold/realtime/aggregates")
    pdf = df.toPandas()
    return jsonify(pdf.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
