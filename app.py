import streamlit as st
import pandas as pd
from analytics import zscore_anomalies

st.set_page_config(page_title="Sensor Dashboard", layout="wide")

# 1. Read data.csv
df = pd.read_csv("data.csv", parse_dates=["timestamp"])

# 2. Detect anomalies
df["temp_anomaly"] = zscore_anomalies(df["temperature"])
df["vib_anomaly"] = zscore_anomalies(df["vibration"])

# 3. Display line charts side by side
col1, col2 = st.columns(2)
with col1:
    st.line_chart(df.set_index("timestamp")["temperature"], height=300, use_container_width=True)
    st.caption("Temperature over time")
with col2:
    st.line_chart(df.set_index("timestamp")["vibration"], height=300, use_container_width=True)
    st.caption("Vibration over time")

# 4. Show last 10 readings
st.subheader("Last 10 Readings")
st.dataframe(df.tail(10)[["timestamp", "temperature", "vibration"]].reset_index(drop=True))

# 5. Display anomaly counts and status
temp_anom_count = df["temp_anomaly"].sum()
vib_anom_count = df["vib_anomaly"].sum()
st.metric("Temperature Anomalies", int(temp_anom_count))
st.metric("Vibration Anomalies", int(vib_anom_count))

if temp_anom_count > 0 or vib_anom_count > 0:
    st.error("⚠️ Anomalies detected! Please investigate.")
else:
    st.success("✅ All systems normal.")