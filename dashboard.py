# dashboard.py
import streamlit as st
import sqlite3
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="NoChai Heatmap", layout="wide")
st.title("🔥 NoChai — Kenya Corruption Heatmap")
st.markdown("Real-time anonymous reports from citizens refusing bribes")

# Load data
conn = sqlite3.connect("nochai.db")
df = pd.read_sql_query("SELECT * FROM reports ORDER BY timestamp DESC", conn)
conn.close()

# Kenyan location coordinates
coords = {
    "Nairobi": [-1.2921, 36.8219],
    "Kisumu": [-0.0917, 34.7680],
    "Mombasa": [-4.0435, 39.6682],
    "Eldoret": [0.5143, 35.2698],
    "Nakuru": [-0.3031, 36.0800],
    "Githurai": [-1.2040, 36.9120],
    "Kitui": [-1.3672, 38.0106],
    "Unknown": [-1.2864, 36.8172]
}

df["lat"] = df["location"].apply(lambda x: coords.get(x, coords["Unknown"])[0])
df["lon"] = df["location"].apply(lambda x: coords.get(x, coords["Unknown"])[1])

col1, col2 = st.columns([1, 2])
with col1:
    st.metric("Total Reports", len(df))
    st.metric("Total Bribes Refused", f"KSh {df['amount'].sum():,.0f}")
    st.dataframe(df[["timestamp", "location", "amount", "category"]].head(10))

with col2:
    m = folium.Map(location=[-1.2864, 36.8172], zoom_start=6, tiles="CartoDB positron")
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=min(row["amount"]/50, 15),
            color="#ff4b4b",
            fill=True,
            popup=f"{row['location']} • KSh {row['amount']}"
        ).add_to(m)
    st_folium(m, width=700, height=500)

st.caption("Built for Kenya AI Hackathon 2025 | NoChai.Refuse. Report. Reclaim.")