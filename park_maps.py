import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

def render_park_details(parks_df: pd.DataFrame):
    st.subheader("Parks Details")
    if parks_df is None or parks_df.empty:
        st.info("No park records are available. Add a parks dataset with name, latitude and longitude columns.")
        return

    required = {"name","latitude","longitude"}
    missing = required - set(parks_df.columns)
    if missing:
        st.error(f"Park map requires columns: {', '.join(sorted(required))}. Missing: {', '.join(sorted(missing))}")
        return

    names = parks_df["name"].dropna().astype(str).tolist()
    selected = st.selectbox("Select a park for details", names)
    row = parks_df[parks_df["name"].astype(str) == selected].iloc[0]

    lat, lon = float(row["latitude"]), float(row["longitude"])
    m = folium.Map(location=[lat, lon], zoom_start=13, control_scale=True)
    popup = folium.Popup(f"<b>{selected}</b>", max_width=300)
    folium.Marker([lat, lon], popup=popup, tooltip=selected).add_to(m)

    radius = row.get("radius_m", None)
    if pd.notna(radius) if radius is not None else False:
        folium.Circle([lat, lon], radius=float(radius), fill=False).add_to(m)

    st_folium(m, width=None, height=500)
    details = row.to_frame("value")
    st.dataframe(details, use_container_width=True)
