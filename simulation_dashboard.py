import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from hydrology_engine import rainfall_runoff_simulation
from crop_water_engine import crop_water_requirement
from flood_engine import peak_flow_scenario
from climate_scenario_engine import apply_climate_scenario
from monte_carlo_engine import monte_carlo_risk

def render_simulation_dashboard():
    st.subheader("Engineering Simulation Engines")
    engine = st.selectbox("Simulation engine", [
        "Rainfall–runoff",
        "Crop water requirement",
        "Flood scenario",
        "Climate scenario",
        "Monte Carlo risk"
    ])

    if engine == "Rainfall–runoff":
        rain = st.text_input("Daily rainfall values (mm), comma separated", "20,0,35,50,10")
        area = st.number_input("Catchment area (km²)", 1.0, 1_000_000.0, 1000.0)
        coeff = st.slider("Runoff coefficient", 0.0, 1.0, 0.35)
        arr = [float(x.strip()) for x in rain.split(",") if x.strip()]
        result = rainfall_runoff_simulation(arr, area, coeff)
        st.dataframe(result, use_container_width=True)
        st.plotly_chart(px.line(result, y="runoff_volume_m3", title="Simulated runoff volume"), use_container_width=True)

    elif engine == "Crop water requirement":
        eto = st.text_input("ETo values (mm), comma separated", "120,130,140,150")
        kc = st.text_input("Kc values, comma separated", "0.7,0.9,1.1,0.9")
        rain = st.text_input("Effective rainfall (mm), comma separated", "10,20,5,15")
        eff = st.slider("Irrigation efficiency", 0.1, 1.0, 0.65)
        result = crop_water_requirement([float(x) for x in eto.split(",")], [float(x) for x in kc.split(",")],
                                        [float(x) for x in rain.split(",")], eff)
        st.dataframe(result, use_container_width=True)

    elif engine == "Flood scenario":
        flow = st.text_input("Base flow values (m³/s), comma separated", "100,200,300,400")
        mult = st.slider("Rainfall multiplier", 0.5, 3.0, 1.2)
        result = peak_flow_scenario([float(x) for x in flow.split(",")], mult)
        st.dataframe(result, use_container_width=True)

    elif engine == "Climate scenario":
        scenario = st.selectbox("Scenario", ["Low","Moderate","High"])
        df = pd.DataFrame({
            "temperature_c":[20,22,24,26],
            "precipitation_mm":[30,40,20,50]
        })
        st.dataframe(apply_climate_scenario(df, scenario), use_container_width=True)

    else:
        e = st.slider("Exposure", 0, 100, 50)
        v = st.slider("Population vulnerability", 0, 100, 50)
        s = st.slider("Sensitivity", 0, 100, 50)
        a = st.slider("Adaptive capacity", 0, 100, 50)
        n = st.number_input("Monte Carlo iterations", 100, 100000, 5000)
        result = monte_carlo_risk(int(n), e, v, s, a)
        st.metric("Mean simulated risk", f"{result['risk'].mean():.1f}")
        st.plotly_chart(px.histogram(result, x="risk", nbins=40, title="Risk distribution"), use_container_width=True)
