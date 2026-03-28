import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("aircraft_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# -----------------------------
# TITLE
# -----------------------------
st.title("Aircraft Monitoring Dashboard")
st.write("This dashboard visualizes aircraft data over Perak, including altitude trends, aircraft count, and flight paths.")

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.header("Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# FILTER
# -----------------------------
st.header("Filter Aircraft")

aircraft_list = df["icao24"].unique()
selected_aircraft = st.selectbox("Select Aircraft", aircraft_list)

filtered_df = df[df["icao24"] == selected_aircraft]

# -----------------------------
# ALTITUDE GRAPH
# -----------------------------
st.header("Altitude Over Time")

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
# FLIGHT PATH MAP
# -----------------------------
st.header("Flight Path Map")

m = folium.Map(location=[4.5, 101.0], zoom_start=7)

for aircraft in df["icao24"].unique():
    path = df[df["icao24"] == aircraft]
    
    coords = path[["latitude", "longitude"]].dropna().values.tolist()
    
    if len(coords) > 1:
        folium.PolyLine(coords).add_to(m)

st_folium(m, width=700, height=500)

# -----------------------------
# INSIGHTS
# -----------------------------
st.header("Insights")

peak_time = df.groupby(df["timestamp"].dt.hour).size().idxmax()
peak_count = df.groupby(df["timestamp"].dt.hour).size().max()

st.write(f"Peak traffic occurs at hour: {peak_time}:00")
st.write(f"Maximum number of aircraft observed: {peak_count}")

