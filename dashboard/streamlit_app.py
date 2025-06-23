import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import pandas as pd
import time
from delta import configure_spark_with_delta_pip

st.set_page_config(page_title="Gold Real-Time Dashboard", layout="wide")
REFRESH_INTERVAL_SEC = 10
st.experimental_set_query_params(t=int(time.time()))  # Triggers rerun: Old version! I have to fix it 

# Set chart title and refresh indicator
st.title("Gold Aggregates Dashboard (Live)")
st.markdown(f"⏱️ Refreshing every **{REFRESH_INTERVAL_SEC} seconds**.")


@st.cache_resource
def get_spark():
    builder = (
        SparkSession.builder.appName("GoldDashboard")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()

spark = get_spark()
df = spark.read.format("delta").load("/mnt/s3mock/gold/realtime/aggregates")
pdf = df.toPandas()

# Visuals
st.dataframe(pdf)

st.line_chart(pdf.set_index("event_date")[["unique_users"]])
st.bar_chart(pdf.groupby("event_type")["event_count"].sum())

# Auto-refresh using JavaScript (instead of manual reload)
st.markdown(
    f"""
    <script>
    setTimeout(function() {{
        window.location.reload();
    }}, {REFRESH_INTERVAL_SEC * 1000});
    </script>
    """,
    unsafe_allow_html=True,
)
