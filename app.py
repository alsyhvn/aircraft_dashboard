import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# Load data
df = pd.read_csv("aircraft_data.csv")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

st.title("Aircraft Monitoring Dashboard")

# -----------------------------
# ALTITUDE GRAPH
# -----------------------------
st.header("Altitude Over Time")

aircraft_list = df["icao24"].unique()
selected_aircraft = st.selectbox("Select Aircraft", aircraft_list)

filtered_df = df[df["icao24"] == selected_aircraft]

plt.figure()
plt.plot(filtered_df["timestamp"], filtered_df["altitude"])
plt.xlabel("Time")
plt.ylabel("Altitude")
plt.title("Altitude Change")
st.pyplot(plt)

# -----------------------------
# AIRCRAFT COUNT
# -----------------------------
st.header("Aircraft Count Over Time")

df["minute"] = df["timestamp"].dt.floor("min")
count_df = df.groupby("minute").size()

plt.figure()
plt.plot(count_df.index, count_df.values)
plt.xlabel("Time")
plt.ylabel("Number of Aircraft")
plt.title("Aircraft Count Over Time")
st.pyplot(plt)

# -----------------------------
# MAP
# -----------------------------
st.header("Flight Path Map")

m = folium.Map(location=[4.5, 101.0], zoom_start=7)

for _, row in df.iterrows():
    if pd.notnull(row["latitude"]) and pd.notnull(row["longitude"]):
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=2
        ).add_to(m)

st_folium(m, width=700, height=500)
