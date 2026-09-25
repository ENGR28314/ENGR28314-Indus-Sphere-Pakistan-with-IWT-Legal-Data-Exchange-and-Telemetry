import pandas as pd
import plotly.express as px
import streamlit as st

METRICS = {
    "Cultivated area (ha)": "cultivated_area",
    "Crop production (tonnes)": "crop_production",
    "Employment (persons)": "employment",
    "Honey production (tonnes)": "honey_production",
    "Aquaculture production (tonnes)": "aquaculture_production",
}

def render_socio_economic():
    st.subheader("Socio-Economic Domain")
    st.caption("All displayed values are input-driven. No final result is hard-coded.")

    default = pd.DataFrame({
        "province_region": ["Punjab","Sindh","Khyber Pakhtunkhwa","Balochistan","Gilgit-Baltistan","Azad Jammu and Kashmir","Islamabad Capital Territory"],
        "cultivated_area": [0.0]*7,
        "crop_production": [0.0]*7,
        "employment": [0.0]*7,
        "honey_production": [0.0]*7,
        "aquaculture_production": [0.0]*7,
    })

    uploaded = st.file_uploader("Upload socio/agro CSV/XLS/XLSX", type=["csv","xls","xlsx"], key="socio_upload")
    if uploaded:
        try:
            df = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
        except Exception as e:
            st.error(f"Could not read the dataset: {e}")
            return
    else:
        df = default

    df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="socio_editor")
    graph_type = st.selectbox("Graph type", ["Bar chart","Pie chart","Scatter plot","Line chart"], key="socio_graph")
    metric = st.selectbox("Metric", list(METRICS.keys()), key="socio_metric")
    col = METRICS[metric]

    if col not in df.columns or "province_region" not in df.columns:
        st.error("Required columns are missing.")
        return
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if graph_type == "Bar chart":
        fig = px.bar(df, x="province_region", y=col, title=metric)
    elif graph_type == "Pie chart":
        fig = px.pie(df, names="province_region", values=col, title=metric)
    elif graph_type == "Scatter plot":
        fig = px.scatter(df, x="province_region", y=col, size=col, title=metric)
    else:
        fig = px.line(df, x="province_region", y=col, markers=True, title=metric)
    st.plotly_chart(fig, use_container_width=True)
