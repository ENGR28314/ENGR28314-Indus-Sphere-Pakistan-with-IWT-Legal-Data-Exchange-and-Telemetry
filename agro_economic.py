import pandas as pd
import plotly.express as px
import streamlit as st

RABI = [
    {"season":"Rabi","crop":"Wheat","typical_window":"October–April",
     "engineering_water_note":"Cool-season crop; irrigation demand is concentrated during establishment, tillering and grain filling."},
    {"season":"Rabi","crop":"Gram (Chickpea)","typical_window":"October–March",
     "engineering_water_note":"Generally lower irrigation demand than wheat; scheduling depends strongly on soil moisture and rainfall."},
    {"season":"Rabi","crop":"Mustard/Rapeseed","typical_window":"October–March",
     "engineering_water_note":"Moderate seasonal water requirement; avoid excessive irrigation near maturity."},
    {"season":"Rabi","crop":"Barley","typical_window":"October–March",
     "engineering_water_note":"Cool-season cereal; irrigation scheduling should account for soil storage and rainfall."},
]
KHARIF = [
    {"season":"Kharif","crop":"Rice","typical_window":"May–October",
     "engineering_water_note":"High water-management sensitivity; irrigation and drainage scheduling should reflect soil, climate and production system."},
    {"season":"Kharif","crop":"Cotton","typical_window":"April–October",
     "engineering_water_note":"Irrigation timing should prioritize establishment, flowering and boll development while avoiding waterlogging."},
    {"season":"Kharif","crop":"Maize","typical_window":"April–September",
     "engineering_water_note":"Water demand varies by hybrid and planting date; flowering and grain filling are sensitive stages."},
    {"season":"Kharif","crop":"Sugarcane","typical_window":"Year-round / seasonal planting",
     "engineering_water_note":"Long-duration crop with substantial cumulative water demand; irrigation efficiency is important."},
]

APICULTURE = [
    {"indicator":"Honey production","unit":"tonnes","description":"Reported or user-entered honey output."},
    {"indicator":"Apiary units","unit":"count","description":"Number of managed apiary units or colonies."},
    {"indicator":"Employment","unit":"persons","description":"Direct employment associated with apiculture activities."},
]
AQUACULTURE = [
    {"indicator":"Aquaculture production","unit":"tonnes","description":"Reported or user-entered farmed aquatic production."},
    {"indicator":"Aquaculture farms","unit":"count","description":"Number of aquaculture production units."},
    {"indicator":"Employment","unit":"persons","description":"Direct employment associated with aquaculture activities."},
]

METRICS = {
    "Cultivated area (ha)": "cultivated_area",
    "Crop production (tonnes)": "crop_production",
    "Employment (persons)": "employment",
    "Honey production (tonnes)": "honey_production",
    "Aquaculture production (tonnes)": "aquaculture_production",
}

def empty_agro_df():
    return pd.DataFrame({
        "province_region": pd.Series(dtype="string"),
        "cultivated_area": pd.Series(dtype="float"),
        "crop_production": pd.Series(dtype="float"),
        "employment": pd.Series(dtype="float"),
        "honey_production": pd.Series(dtype="float"),
        "aquaculture_production": pd.Series(dtype="float"),
    })

def render_agro_economic():
    st.subheader("Agro-Economic Domain")
    st.markdown("### Major crop seasons")
    st.dataframe(pd.DataFrame(RABI + KHARIF), use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Rabi")
        st.dataframe(pd.DataFrame(RABI), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("#### Kharif")
        st.dataframe(pd.DataFrame(KHARIF), use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Apiculture")
        st.dataframe(pd.DataFrame(APICULTURE), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("### Aquaculture")
        st.dataframe(pd.DataFrame(AQUACULTURE), use_container_width=True, hide_index=True)

    st.markdown("### Input-driven socio/agro data")
    if "agro_rows" not in st.session_state:
        st.session_state.agro_rows = empty_agro_df()

    uploaded = st.file_uploader(
        "Upload CSV/XLS/XLSX socio/agro data",
        type=["csv","xls","xlsx"],
        key="agro_upload"
    )
    if uploaded:
        try:
            if uploaded.name.lower().endswith(".csv"):
                st.session_state.agro_rows = pd.read_csv(uploaded)
            else:
                st.session_state.agro_rows = pd.read_excel(uploaded)
            st.success("Dataset loaded.")
        except Exception as e:
            st.error(f"Could not read the dataset: {e}")

    edited = st.data_editor(
        st.session_state.agro_rows,
        num_rows="dynamic",
        use_container_width=True,
        key="agro_editor"
    )
    st.session_state.agro_rows = edited

    if not edited.empty:
        graph_type = st.selectbox("Graph type", ["Bar chart","Pie chart","Scatter plot","Line chart"], key="agro_graph")
        metric = st.selectbox("Metric", list(METRICS.keys()), key="agro_metric")
        col = METRICS[metric]
        if col not in edited.columns:
            st.warning(f"Column '{col}' is required for this metric.")
            return
        plot_df = edited.copy()
        plot_df[col] = pd.to_numeric(plot_df[col], errors="coerce").fillna(0)
        if "province_region" not in plot_df.columns:
            st.warning("Column 'province_region' is required.")
            return
        if graph_type == "Bar chart":
            fig = px.bar(plot_df, x="province_region", y=col, title=metric)
        elif graph_type == "Pie chart":
            fig = px.pie(plot_df, names="province_region", values=col, title=metric)
        elif graph_type == "Scatter plot":
            fig = px.scatter(plot_df, x="province_region", y=col, size=col, title=metric)
        else:
            fig = px.line(plot_df, x="province_region", y=col, markers=True, title=metric)
        st.plotly_chart(fig, use_container_width=True)
