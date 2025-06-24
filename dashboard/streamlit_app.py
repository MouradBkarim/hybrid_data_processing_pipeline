import requests
import pandas as pd
import streamlit as st
import time

st.set_page_config(page_title="Gold Real-Time Dashboard", layout="wide")
REFRESH_INTERVAL_SEC = 10

st.title("Gold Aggregates Dashboard (Live)")
st.markdown(f"Refreshing every **{REFRESH_INTERVAL_SEC} seconds**.")

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

try:
    res = requests.get("http://notebook:9999/api/gold-aggregates", timeout=5)
    if res.status_code != 200:
        st.error(f"API returned {res.status_code}: {res.text}")
        st.stop()
    data = res.json()
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"Failed to fetch or parse data: {e}")
    st.stop()

st.dataframe(df)

if "event_date" in df.columns and "unique_users" in df.columns:
    st.line_chart(df.set_index("event_date")[["unique_users"]])
if "event_type" in df.columns and "event_count" in df.columns:
    st.bar_chart(df.groupby("event_type")["event_count"].sum())
