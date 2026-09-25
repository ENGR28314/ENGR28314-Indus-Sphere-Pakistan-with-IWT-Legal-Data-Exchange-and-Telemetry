import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import *
from expanded_inventory import *
from development_framework import sdg_table, mdg_table, vision_table, crosswalk_table, DEVELOPMENT_DOMAINS
from data_analytics import load_uploaded_file, coerce_numeric, chart_candidates
from water_quality_analytics import (
    detect_basin_column, detect_telemetry_columns, detect_water_quality_columns,
    telemetry_variance_by_basin, water_quality_summary, generate_visualization_script,
)
from socio_agro_inputs import (CROP_SEASONS, APICULTURE, AQUACULTURE, CROP_MATRIX,
    APICULTURE_INDICATORS, AQUACULTURE_INDICATORS, DEFAULT_SOCIO_AGRO, SOCIO_AGRO_COLUMNS)
import map_view
from map_view import water_map
from network_view import river_network
from hydraulic_model import scenario_summary
from simulation_engine import ENGINES
from pca_timeline import pca_timeline_df, PCA_VALIDITY_NOTE
from india_water_projects import projects_df, engineering_df, PAKISTAN_POSITION
from hydrology_engine import monthly_water_balance, reservoir_rule_curve
from flood_engine import flood_scenario, rainfall_sweep
from crop_water_engine import crop_comparison, CROP_COEFFICIENTS
from climate_engine import climate_stress, sensitivity_table
from monte_carlo_engine import monte_carlo_risk, summarize
from iwt_compliance_engine import ExchangeRecord, compliance_matrix, gap_score, ARTICLE_BASELINE
from iwt_data_exchange_engine import normalize_exchange_df, compare_dataset_coverage, empty_template
from iwt_timeline_engine import timeline_df
from iwt_dispute_resolution_engine import pathway
from iwt_evidence_engine import evidence_ledger
from iwt_scenario_engine import scenario_matrix

st.set_page_config(
    page_title="IndusSphere Pakistan",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="expanded",
)

CREATOR = "Engr. Syed Hassan Iqbal Shah"

# ---------------------------------------------------------------------------
# Visual styling — modeled on the classic Pakistan Water/Terrain Explorer
# layout: branded sidebar navigation, wide content area, cards and tables.
# ---------------------------------------------------------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
[data-testid="stSidebar"] {min-width: 285px; max-width: 320px;}
.hero {
    padding: 1.1rem 1.35rem; border-radius: 14px; margin-bottom: 1rem;
    border: 1px solid rgba(49,51,63,.15);
    background: linear-gradient(135deg, rgba(27,94,32,.10), rgba(25,118,210,.08));
}
.hero h1 {margin-bottom:.2rem;}
.small-note {font-size:.86rem; opacity:.75;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def filter_df(df, province="All", search=""):
    x = df.copy()
    if province != "All" and not x.empty:
        cols = [c for c in ["province_region", "region", "province", "territory", "area"] if c in x.columns]
        if cols:
            mask = pd.Series(False, index=x.index)
            for c in cols:
                mask = mask | x[c].astype(str).str.contains(province, case=False, na=False)
            x = x[mask]
    if search.strip() and not x.empty:
        q = search.strip()
        mask = x.astype(str).apply(lambda col: col.str.contains(q, case=False, na=False)).any(axis=1)
        x = x[mask]
    return x


def show_table(df, columns=None):
    x = df.copy()
    if columns:
        columns = [c for c in columns if c in x.columns]
        if columns:
            x = x[columns]
    st.dataframe(x, use_container_width=True, hide_index=True)


# ---------------------------------------------------------------------------
# Sidebar — intentionally mirrors the reference explorer's navigation model.
# ---------------------------------------------------------------------------
SECTIONS = [
    "🏠 Overview",
    "🗺️ Provinces & Territories",
    "🌊 Rivers",
    "🚧 Dams & Barrages",
    "🔀 Link Canals",
    "🌡️ Climatic Regions",
    "⛰️ Mountain Ranges",
    "🏞️ Lakes",
    "🏜️ Deserts",
    "⚠️ Disaster Risk Context",
    "📈 Socio-Economic & Agro-Economic",
    "🗺️ Geo-Political & Strategic",
    "🇨🇳 China Hydropower (CPEC)",
    "📐 India Upstream Dam Disputes",
    "🇮🇳 Indian Atrocities",
    "⚖️ IWT Legal & Data Exchange",
    "🌲 Forests & Parks",
    "🌍 SDGs / MDGs / Vision 2030",
    "🧮 Interactive Hydraulic Models",
    "⚙️ Simulation Engines",
    "📊 Data Analytics & Graphs",
    "🧭 Regional Profiles",
    "📚 Sources",
]

with st.sidebar:
    st.markdown("# 🇵🇰 IndusSphere")
    st.caption("Pakistan Water, Terrain, Climate & Strategic Explorer")
    st.markdown(f"**Creator:** {CREATOR}")
    st.divider()
    choice = st.radio("Go to section", SECTIONS, label_visibility="collapsed")
    st.divider()
    st.header("🔎 Global Filters")
    province = st.selectbox("Province / Region", ["All"] + list(PROVINCES))
    search = st.text_input("Search inventory", placeholder="river, dam, lake, forest...")
    st.divider()
    st.header("🧮 Scenario Inputs")
    exposure = st.slider("Exposure", 0, 100, 60)
    vulnerability = st.slider("Population vulnerability", 0, 100, 55)
    sensitivity = st.slider("Sensitivity", 0, 100, 55)
    adaptive = st.slider("Adaptive capacity", 0, 100, 50)
    criticality = st.slider("Asset / service criticality", 0, 100, 65)
    scenario = st.selectbox("Scenario", ["Baseline", "Medium", "Worst-Case"])
    st.divider()
    st.caption("Built with Streamlit · Pandas · Plotly")

st.markdown(f"""
<div class="hero">
<h1>🇵🇰 IndusSphere Pakistan</h1>
<div>Integrated Water, Terrain, Climate, Disaster-Risk, Socio-Economic & Strategic Intelligence Explorer</div>
<div class="small-note">Creator: {CREATOR}</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
if choice == "🏠 Overview":
    st.title("Pakistan Water, Terrain & Integrated Intelligence Explorer")
    st.write("Interactive national-scale exploration of Pakistan's water systems, terrain, climate, hazards, economy, agriculture and strategic infrastructure.")
    cols = st.columns(6)
    metrics = [
        ("Regions", len(PROVINCES)), ("Rivers", len(RIVERS)),
        ("Dams", len(DAMS)), ("Barrages", len(BARRAGES)),
        ("Lakes", len(LAKES) + len(EXTRA_LAKES)), ("Parks", len(NATIONAL_PARKS) + len(EXTRA_PARKS)),
    ]
    for col, (label, value) in zip(cols, metrics): col.metric(label, value)
    st.subheader("National water and terrain view")
    st.plotly_chart(water_map(filter_df(RIVERS, province, search), filter_df(DAMS, province, search), filter_df(BARRAGES, province, search), filter_df(CONFLUENCES, province, search)), use_container_width=True)
    st.subheader("Regional overview")
    show_table(filter_df(REGIONAL_PROFILE, province, search))
    st.info("Map points are curated visualization coordinates. Verify authoritative GIS, engineering and survey data before professional use.")

elif choice == "🗺️ Provinces & Territories":
    st.title("Provinces & Territories of Pakistan")
    show_table(filter_df(REGIONAL_PROFILE, province, search))
    st.subheader("Major cities / service centres")
    show_table(filter_df(MAJOR_CITIES, province, search))

elif choice == "🌊 Rivers":
    st.title("Rivers of Pakistan")
    st.plotly_chart(river_network(), use_container_width=True)
    show_table(filter_df(RIVERS, province, search), ["name","river_system","province_region","upstream","downstream","confluences","notes"])
    st.download_button("⬇️ Download rivers CSV", filter_df(RIVERS, province, search).to_csv(index=False).encode(), "indussphere_rivers.csv", "text/csv")
    st.subheader("River confluences")
    show_table(filter_df(CONFLUENCES, province, search))

elif choice == "🚧 Dams & Barrages":
    st.title("Dams, Barrages & Hydropower Projects")
    st.subheader("Dams / hydropower structures")
    show_table(filter_df(DAMS, province, search))
    st.subheader("Barrages / headworks")
    show_table(filter_df(BARRAGES, province, search))
    st.subheader("Upstream / downstream relationships")
    rel = pd.concat([filter_df(DAMS, province, search), filter_df(BARRAGES, province, search)], ignore_index=True)
    show_table(rel, ["name","river","province_region","upstream","downstream","status","notes"])

elif choice == "🔀 Link Canals":
    st.title("Link Canals — Indus Basin Irrigation System (IBIS)")
    st.write("Link canals redistribute water between river systems and irrigation commands within the Indus Basin network.")
    show_table(filter_df(LINK_CANALS, province, search))

elif choice == "🌡️ Climatic Regions":
    st.title("Climatic Regions of Pakistan")
    show_table(pd.DataFrame(CLIMATE_REGIONS))
    if "region" in pd.DataFrame(CLIMATE_REGIONS).columns:
        region_options = pd.DataFrame(CLIMATE_REGIONS)["region"].dropna().tolist()
        if region_options:
            selected = st.selectbox("Climate region detail", region_options)
            row = pd.DataFrame(CLIMATE_REGIONS)
            st.dataframe(row[row["region"] == selected], use_container_width=True, hide_index=True)

elif choice == "⛰️ Mountain Ranges":
    st.title("Mountain Ranges of Pakistan")
    m = filter_df(MOUNTAINS, province, search)
    show_table(m)
    if not m.empty and "name" in m.columns:
        selected = st.selectbox("Select mountain range", m["name"].tolist())
        row = m[m["name"] == selected].iloc[0]
        st.subheader(selected)
        a,b = st.columns(2)
        for i,(k,v) in enumerate(row.items()):
            (a if i % 2 == 0 else b).markdown(f"**{k.replace('_',' ').title()}:** {v}")

elif choice == "🏞️ Lakes":
    st.title("Lakes of Pakistan")
    lakes = pd.concat([LAKES, EXTRA_LAKES], ignore_index=True).drop_duplicates(subset=["name"])
    lakes = filter_df(lakes, province, search)
    st.metric("Inventory entries", len(lakes))
    show_table(lakes)
    st.download_button("⬇️ Download lakes CSV", lakes.to_csv(index=False).encode(), "indussphere_lakes.csv", "text/csv")

elif choice == "🏜️ Deserts":
    st.title("Deserts of Pakistan")
    show_table(filter_df(DESERTS, province, search))

elif choice == "⚠️ Disaster Risk Context":
    st.title("National Disaster Risk Context")
    t1,t2,t3,t4,t5 = st.tabs(["Hydro-meteorological","Tectonic","Climatological / Emerging","Anthropogenic","Exposure & Vulnerability"])
    with t1:
        items = HAZARDS.get("Hydro-meteorological", [])
        show_table(pd.DataFrame(items))
    with t2:
        show_table(pd.DataFrame(HAZARDS.get("Tectonic", [])))
    with t3:
        show_table(pd.DataFrame(HAZARDS.get("Climatological / Emerging", [])))
        show_table(EMERGING_CLIMATE)
    with t4:
        show_table(pd.DataFrame(HAZARDS.get("Anthropogenic", [])))
    with t5:
        show_table(DISASTER_VULNERABILITY)
    st.subheader("Scenario definitions")
    show_table(SCENARIO_DETAIL)

elif choice == "📈 Socio-Economic & Agro-Economic":
    st.title("Socio-Economic & Agro-Economic Domains")
    a,b = st.tabs(["Socio-Economic","Agro-Economic"])
    with a:
        for k,v in SOCIO_ECONOMIC.items(): st.markdown(f"**{k}:** {v}")
        st.subheader("Input-driven socio/agro analytics")
        st.caption("Edit the values below. Every chart is regenerated from the values entered by the user.")
        socio = st.data_editor(pd.DataFrame(DEFAULT_SOCIO_AGRO, columns=SOCIO_AGRO_COLUMNS), num_rows="dynamic", use_container_width=True, key="socio_editor")
        graph_type = st.selectbox("Graph type", ["Bar chart","Pie chart","Scatter plot","Line chart"], key="socio_graph")
        metric_options = SOCIO_AGRO_COLUMNS[1:]
        metric = st.selectbox("Metric", metric_options, key="socio_metric")
        if graph_type == "Scatter plot":
            x = st.selectbox("X-axis", metric_options, index=0, key="socio_x")
            y = st.selectbox("Y-axis", metric_options, index=min(1,len(metric_options)-1), key="socio_y")
            fig = px.scatter(socio, x=x, y=y, hover_name="Province / Region", title=f"{y} vs {x}")
        elif graph_type == "Bar chart": fig = px.bar(socio, x="Province / Region", y=metric, title=metric)
        elif graph_type == "Pie chart": fig = px.pie(socio, names="Province / Region", values=metric, title=metric)
        else: fig = px.line(socio, x="Province / Region", y=metric, markers=True, title=metric)
        st.plotly_chart(fig, use_container_width=True)
        st.download_button("⬇️ Download edited socio/agro data", socio.to_csv(index=False).encode(), "socio_agro_input_data.csv", "text/csv", key="download_socio")
    with b:
        for k,v in AGRO_ECONOMIC.items(): st.markdown(f"**{k}:** {v}")
        st.subheader("Major crop seasons")
        st.dataframe(pd.DataFrame(CROP_MATRIX), use_container_width=True, hide_index=True)
        season = st.selectbox("Season", ["Rabi","Kharif"], key="agro_season")
        st.dataframe(pd.DataFrame([r for r in CROP_MATRIX if r["season"] == season]), use_container_width=True, hide_index=True)
        st.subheader("Rabi")
        st.dataframe(pd.DataFrame(CROP_SEASONS["Rabi"]["crops"], columns=["crop"]).assign(season="Rabi", typical_window=CROP_SEASONS["Rabi"]["period"], engineering_water_note=CROP_SEASONS["Rabi"]["water_focus"]), use_container_width=True, hide_index=True)
        st.subheader("Kharif")
        st.dataframe(pd.DataFrame(CROP_SEASONS["Kharif"]["crops"], columns=["crop"]).assign(season="Kharif", typical_window=CROP_SEASONS["Kharif"]["period"], engineering_water_note=CROP_SEASONS["Kharif"]["water_focus"]), use_container_width=True, hide_index=True)
        st.subheader("Apiculture")
        st.dataframe(pd.DataFrame(APICULTURE_INDICATORS), use_container_width=True, hide_index=True)
        st.subheader("Aquaculture")
        st.dataframe(pd.DataFrame(AQUACULTURE_INDICATORS), use_container_width=True, hide_index=True)

elif choice == "🗺️ Geo-Political & Strategic":
    st.title("Geo-Political & Strategic Domains")
    for k,v in GEO_STRATEGIC.items():
        with st.expander(k, expanded=False): st.write(v)
    st.warning("The dashboard presents documented issues and competing claims neutrally. It does not rank political positions or decide disputed questions.")

elif choice == "🇨🇳 China Hydropower (CPEC)":
    st.title("The Financial Footprint of China's Investments in Pakistan's Hydropower")
    show_table(CHINA_HYDRO)
    st.caption("Project status and financing details are time-sensitive; verify against the linked primary institutional sources.")

elif choice == "📐 India Upstream Dam Disputes":
    st.title("Pakal Dul & Ratle — Technical Issues in the Indus Waters Proceedings")
    show_table(IWT_TECHNICAL)
    st.markdown("The dashboard presents technical issues such as pondage capacity, freeboard/dam elevation, deep-level outlets and gated spillways as documented in the proceedings. Legal conclusions should be taken from the primary PCA materials.")


elif choice == "🇮🇳 Indian Atrocities":
    st.title("🇮🇳 Indian Atrocities — Chenab Projects, Flow Concerns & Indus Waters Treaty")
    st.warning("This tab uses the requested title, but the dashboard presents the underlying water-policy, engineering and legal claims as documented facts or attributed positions rather than as an independent political judgment.")
    st.subheader("1(A) Reported canal / inter-basin transfer proposals")
    st.dataframe(projects_df(), use_container_width=True, hide_index=True)
    st.markdown("The 113-km proposal was reported by NDTV on 16 June 2025 as a feasibility-stage plan to link the Chenab with the Ravi-Beas-Sutlej system. The report said the work was preliminary and feasibility reports were being prepared. urlNDTV reporthttps://www.ndtv.com/india-news/a-113-km-long-canal-inside-indias-big-indus-waters-treaty-plan-8683486")
    st.subheader("1(B) Chenab hydropower projects")
    st.dataframe(projects_df()[projects_df()["category"] == "Hydropower"], use_container_width=True, hide_index=True)
    st.caption("India's Ministry of Power reported in January 2026 that Pakal Dul is 1,000 MW, Kiru 624 MW and Kwar 540 MW, with stated commissioning targets for Pakal Dul/Kiru in December 2026 and Kwar in March 2028. citeturn2view3")
    st.subheader("Pakistan's stated concerns")
    for item in PAKISTAN_POSITION: st.markdown(f"• {item}")
    st.subheader("2(A) Disputed engineering specifications")
    st.dataframe(engineering_df(), use_container_width=True, hide_index=True)
    st.info("The PCA's public case record lists awards on competence, general interpretation, maximum pondage, treaty status and an interim-measures order concerning Ratle. The dashboard does not substitute its own legal conclusion for those primary records. citeturn0search3turn0search1")
    st.subheader("2(B) Neutral Expert timeline & practical impact")
    st.markdown("**Publicly reported milestone:** final Neutral Expert determination is expected in July 2027 in current summaries. The PCA case record separately identifies the Neutral Expert proceedings as a parallel proceeding under the IWT. citeturn0search3turn0search5")
    st.dataframe(pd.DataFrame([
        {"Milestone":"Nov 2026","Description":"Synthesis memorandum / modelling work — use only as a planning reference until confirmed in the latest procedural record."},
        {"Milestone":"Feb 2027","Description":"Further meeting / hydraulic modelling milestone reported in supplied material."},
        {"Milestone":"Mar 2027","Description":"Draft technical decision circulation reported in supplied material."},
        {"Milestone":"Jul 2027","Description":"Expected final Neutral Expert determination referenced by ASIL's summary of the 31 Aug 2026 proceedings."},
    ]), use_container_width=True, hide_index=True)
    st.caption("Procedural dates beyond the publicly verified July 2027 expectation should be checked against the latest World Bank/PCA procedural documents before being treated as binding dates.")

elif choice == "⚖️ IWT Legal & Data Exchange":
    st.title("⚖️ Indus Waters Treaty — Legal Baseline & Data-Exchange Explorer")
    st.write("An evidence-driven research and simulation workspace for examining IWT data-exchange records, institutional channels, timelines and dispute-resolution pathways. It does not determine whether a treaty violation occurred.")
    st.warning("Legal-status outputs are descriptive screening indicators. Treaty interpretation and compliance conclusions should be taken from the treaty text, applicable awards/orders, and verified evidence.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Legal Baseline", "Exchange Audit", "Timeline", "Resolution Pathways", "Evidence & Scenarios"])
    with tab1:
        st.subheader("Core treaty provisions")
        st.dataframe(pd.DataFrame([{"Provision":k,"Baseline":v} for k,v in ARTICLE_BASELINE.items()]), use_container_width=True, hide_index=True)
        st.markdown("**Key analytical principle:** examine the content of information, reporting frequency, and institutional channel separately before drawing any conclusion.")
        st.info("The app deliberately distinguishes treaty text, party positions, adjudicative findings, observed hydrological records and model-generated indicators.")

    with tab2:
        st.subheader("Hydrological data-exchange audit")
        st.caption("Enter documented events or upload a prepared exchange CSV. The resulting flags identify documentation gaps; they are not legal findings.")
        mode=st.radio("Input mode", ["Manual record", "CSV upload"], horizontal=True)
        if mode == "Manual record":
            c=st.columns(3)
            date=c[0].text_input("Date", "2026-09-01")
            river=c[1].text_input("River", "Chenab")
            dataset=c[2].text_input("Dataset", "Gauge / discharge")
            c=st.columns(4)
            frequency=c[0].selectbox("Frequency", ["Daily","Monthly","More frequently on request","Ad hoc","Unknown"])
            channel=c[1].selectbox("Transmission channel", ["PIC / Commissioners","Diplomatic channel","Other / unspecified"])
            notice=c[2].selectbox("Prior notice", ["Yes","No","Unknown"])
            source=c[3].text_input("Evidence/source", "User-provided record")
            rec=ExchangeRecord(date,river,dataset,frequency,channel,notice,source)
            result=pd.DataFrame(compliance_matrix([rec]))
            st.dataframe(result, use_container_width=True, hide_index=True)
            st.metric("Documentation-gap indicator", gap_score(rec))
            st.caption("Higher values mean more fields require documentary review; this is not a probability or legal-compliance score.")
        else:
            up=st.file_uploader("Upload exchange records", type=["csv","xlsx","xls"])
            if up:
                try:
                    if up.name.lower().endswith('.csv'): df=pd.read_csv(up)
                    else: df=pd.read_excel(up)
                    norm=normalize_exchange_df(df)
                    st.dataframe(norm,use_container_width=True,hide_index=True)
                    st.subheader("Dataset coverage")
                    cov=compare_dataset_coverage(norm)
                    st.dataframe(cov,use_container_width=True,hide_index=True)
                    st.download_button("Download normalized exchange CSV",norm.to_csv(index=False).encode(),"iwt_exchange_normalized.csv","text/csv")
                except Exception as e: st.error(f"Could not read file: {e}")
            else:
                st.download_button("Download blank exchange template",empty_template().to_csv(index=False).encode(),"iwt_exchange_template.csv","text/csv")

    with tab3:
        st.subheader("IWT research timeline")
        st.info(PCA_VALIDITY_NOTE)
        tl=pca_timeline_df()
        st.plotly_chart(px.scatter(tl,x="date",y="category",text="event",hover_data=["source","status"],title="Selected treaty and arbitration events"),use_container_width=True)
        st.dataframe(tl,use_container_width=True,hide_index=True)
        st.caption("The timeline separates historical facts, PCA records, and expected/procedural milestones. It is not an exhaustive chronology.")

    with tab4:
        st.subheader("Descriptive dispute-resolution pathways")
        issue=st.selectbox("Issue type", ["Data exchange","Technical design issue","Treaty interpretation"])
        rows=[{"Stage":a,"Description":b} for a,b in pathway(issue)]
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        st.info("The appropriate pathway depends on the treaty provisions and characterization of the particular matter; the app does not select a legal forum as a recommendation.")

    with tab5:
        st.subheader("Evidence hierarchy")
        st.dataframe(evidence_ledger(),use_container_width=True,hide_index=True)
        st.subheader("Data-channel scenarios")
        st.dataframe(scenario_matrix(),use_container_width=True,hide_index=True)
        st.subheader("Primary current arbitration record")
        st.markdown("The PCA case record includes the 27 June 2025 Supplemental Award on Competence, 8 August 2025 Award on General Interpretation, 15 May 2026 Maximum Pondage Award, and 31 August 2026 Award on Treaty Status plus Order on Interim Measures.")

elif choice == "🌲 Forests & Parks":
    st.title("Forests, National Parks & Recreational Areas")
    st.subheader("Forest types")
    show_table(FOREST_TYPES)
    st.subheader("Notable forests")
    show_table(filter_df(FORESTS, province, search))

    st.subheader("National parks / protected / recreational areas")
    parks = pd.concat([NATIONAL_PARKS, EXTRA_PARKS], ignore_index=True).drop_duplicates(subset=["name"])
    parks_filtered = filter_df(parks, province, search)

    park_tab1, park_tab2 = st.tabs(["🗺️ Parks Map", "📍 Select a park for details"])
    with park_tab1:
        st.plotly_chart(map_view.parks_map(parks_filtered), use_container_width=True)
        st.caption("Park markers show representative locations for visualization; they are not official park boundaries.")
        show_table(parks_filtered)

    with park_tab2:
        park_names = parks_filtered["name"].tolist()
        if park_names:
            selected_park = st.selectbox("Select a park for details", park_names)
            selected_row = parks_filtered.loc[parks_filtered["name"] == selected_park].iloc[0]
            st.subheader(selected_park)
            c1, c2, c3 = st.columns(3)
            c1.metric("Region", selected_row["province_region"] if "province_region" in selected_row else selected_row.get("region", "—"))
            c2.metric("Location", selected_row["location"])
            c3.metric("Type / Focus", selected_row["focus"])
            st.plotly_chart(map_view.parks_map(parks_filtered, selected_name=selected_park), use_container_width=True)
            st.caption("The star identifies the selected park. The marker is a representative map point, not a surveyed boundary.")
            st.dataframe(pd.DataFrame([selected_row]), use_container_width=True, hide_index=True)
        else:
            st.info("No parks match the current Province/Region or search filters.")

elif choice == "🌍 SDGs / MDGs / Vision 2030":
    st.title("UN SDGs / MDGs / Pakistan Vision 2030")
    view = st.selectbox("Framework", ["SDGs","MDGs","Vision 2030","Crosswalk","Development Domains"])
    if view == "SDGs": show_table(sdg_table())
    elif view == "MDGs": show_table(mdg_table())
    elif view == "Vision 2030": show_table(vision_table())
    elif view == "Crosswalk": show_table(crosswalk_table())
    else: show_table(pd.DataFrame({"Development domain": DEVELOPMENT_DOMAINS}))

elif choice == "🧮 Interactive Hydraulic Models":
    st.title("Interactive Hydraulic & Risk Models")
    result = scenario_summary(exposure, vulnerability, sensitivity, adaptive, scenario)
    a,b,c,d = st.columns(4)
    a.metric("Scenario index", result["risk_index"]); b.metric("Risk class", result["risk_class"]); c.metric("Criticality", criticality); d.metric("Scenario factor", result["scenario_factor"])
    comp = pd.DataFrame({"Component":list(result["components"].keys()),"Value":list(result["components"].values())})
    st.plotly_chart(px.bar(comp, x="Component", y="Value", range_y=[0,100], title="Inputs feeding the scenario index"), use_container_width=True)
    st.write(result["explanation"])
    st.dataframe(pd.DataFrame([{"Scenario":scenario,"Exposure":exposure,"Vulnerability":vulnerability,"Sensitivity":sensitivity,"Adaptive capacity":adaptive,"Criticality":criticality,"Scenario index":result["risk_index"],"Risk class":result["risk_class"]}]), use_container_width=True, hide_index=True)

elif choice == "⚙️ Simulation Engines":
    st.title("⚙️ Engineering Simulation Engines")
    st.write("Run transparent, input-driven screening simulations for reservoirs, floods, crop water requirements, climate stress, uncertainty and river/canal routing. Results are generated from the values entered in the interface.")
    st.info("These are educational/screening models. Professional hydraulic design requires calibrated hydrology, surveyed geometry, boundary conditions and validated engineering software.")
    engine = st.selectbox("Select simulation engine", list(ENGINES.keys()))
    st.caption(f"Engine module: {ENGINES[engine]}")

    if engine == "Reservoir / Water Balance":
        st.subheader("Reservoir mass-balance simulation")
        a,b,c,d=st.columns(4)
        capacity=a.number_input("Reservoir capacity (million m³)",1.0,100000.0,1000.0)
        storage=b.number_input("Initial storage (million m³)",0.0,capacity,600.0)
        evap=c.number_input("Monthly evaporation loss (million m³)",0.0,10000.0,20.0)
        target=d.slider("Target storage fraction",0.0,1.0,0.60,0.05)
        inflow_text=st.text_input("Monthly inflows (million m³, comma separated)","450,500,650,800,900,750,600,500,420,380,400,430")
        demand_text=st.text_input("Monthly demand (million m³, comma separated)","400,420,450,480,500,520,500,480,450,430,410,400")
        try:
            inflow=[float(x.strip()) for x in inflow_text.split(",") if x.strip()]
            demand=[float(x.strip()) for x in demand_text.split(",") if x.strip()]
            if len(inflow)!=len(demand): st.error("Inflow and demand lists must have equal length.")
            else:
                res=reservoir_rule_curve(inflow,demand,capacity,storage,target,evap)
                st.plotly_chart(px.line(res,x="Period",y=["End storage","Target storage"],markers=True,title="Reservoir storage trajectory"),use_container_width=True)
                st.plotly_chart(px.bar(res,x="Period",y=["Inflow","Demand","Release","Shortage"],barmode="group",title="Water balance by period"),use_container_width=True)
                st.dataframe(res,use_container_width=True,hide_index=True)
        except ValueError as e: st.error(str(e))

    elif engine == "Flood Screening":
        st.subheader("Rainfall–runoff and channel-capacity screening")
        a,b,c=st.columns(3)
        rainfall=a.number_input("Rainfall event (mm)",0.0,2000.0,150.0)
        area=b.number_input("Catchment area (km²)",1.0,1000000.0,1000.0)
        runoff=c.slider("Runoff coefficient",0.0,1.0,0.45,0.05)
        d,e,f=st.columns(3)
        capacity=d.number_input("Channel capacity (m³/s)",1.0,1000000.0,500.0)
        duration=e.number_input("Event duration (hours)",0.1,168.0,6.0)
        exposure=f.slider("Exposure",0,100,50)
        vulnerability=st.slider("Vulnerability",0,100,50)
        criticality=st.slider("Asset/service criticality",0,100,50)
        out=flood_scenario(rainfall,area,runoff,capacity,duration,exposure,vulnerability,criticality)
        cols=st.columns(4); cols[0].metric("Runoff volume",f"{out['runoff_volume_m3']:,.0f} m³"); cols[1].metric("Peak-flow proxy",f"{out['peak_flow_proxy_m3s']:,.1f} m³/s"); cols[2].metric("Capacity ratio",f"{out['capacity_ratio']:.2f}×"); cols[3].metric("Risk index",f"{out['risk_index']:.1f}")
        st.write(f"Screening class: **{out['risk_class']}**")
        rain_range=st.slider("Rainfall sensitivity range (mm)",10,1000,(50,500),10)
        sweep=rainfall_sweep(range(rain_range[0],rain_range[1]+1,max(1,(rain_range[1]-rain_range[0])//20 or 1)),catchment_km2=area,runoff_coefficient=runoff,channel_capacity_m3s=capacity,duration_hours=duration,exposure=exposure,vulnerability=vulnerability,criticality=criticality)
        st.plotly_chart(px.line(sweep,x="Rainfall (mm)",y="Peak flow proxy (m3/s)",markers=True,title="Rainfall sensitivity"),use_container_width=True)

    elif engine == "Crop Water Requirement":
        st.subheader("Rabi / Kharif crop water screening")
        season=st.radio("Season",["Rabi","Kharif"],horizontal=True)
        default_crops=["Wheat","Gram/Chickpea","Barley","Mustard/Rapeseed","Canola","Lentil"] if season=="Rabi" else ["Rice","Cotton","Maize","Sugarcane"]
        crops=st.multiselect("Crops",list(CROP_COEFFICIENTS),default=default_crops)
        a,b,c,d=st.columns(4)
        et0=a.number_input("Reference ET0 (mm/season)",0.0,3000.0,600.0)
        rain=b.number_input("Effective rainfall (mm/season)",0.0,2000.0,150.0)
        area_ha=c.number_input("Area (ha)",0.1,1000000.0,100.0)
        eff=d.slider("Irrigation efficiency",0.10,1.0,0.65,0.05)
        if crops:
            cropdf=crop_comparison(crops,et0,rain,area_ha,eff)
            st.plotly_chart(px.bar(cropdf,x="Crop",y="Gross irrigation volume_m3",title="Estimated gross irrigation volume"),use_container_width=True)
            st.dataframe(cropdf,use_container_width=True,hide_index=True)

    elif engine == "Climate Stress":
        st.subheader("Climate scenario and sensitivity simulation")
        vals={}
        cols=st.columns(5)
        for i,k in enumerate(["Exposure","Vulnerability","Sensitivity","Adaptive capacity","Criticality"]): vals[k.lower().replace(" ","_")]=cols[i].slider(k,0,100,50)
        scenario=st.selectbox("Scenario",["Baseline","Medium","Worst-Case"])
        horizon=st.selectbox("Horizon",["Near Term","Mid Century","Long Term"])
        out=climate_stress(vals["exposure"],vals["vulnerability"],vals["sensitivity"],vals["adaptive_capacity"],vals["criticality"],scenario,horizon)
        st.metric("Risk index",f"{out['risk_index']:.1f}"); st.write(f"Class: **{out['risk_class']}** · Scenario factor {out['scenario_factor']} · Horizon factor {out['horizon_factor']}")
        parameter=st.selectbox("Sensitivity parameter",["exposure","vulnerability","sensitivity","adaptive_capacity","criticality"])
        base=dict(exposure=vals["exposure"],vulnerability=vals["vulnerability"],sensitivity=vals["sensitivity"],adaptive_capacity=vals["adaptive_capacity"],criticality=vals["criticality"],scenario=scenario,horizon=horizon)
        sens=sensitivity_table(base,parameter,range(0,101,5))
        st.plotly_chart(px.line(sens,x=parameter,y="Risk index",markers=True,title=f"Risk sensitivity to {parameter.replace('_',' ')}"),use_container_width=True)

    elif engine == "Monte Carlo Risk":
        st.subheader("Monte Carlo uncertainty simulation")
        n=st.slider("Simulation runs",500,10000,2000,500); seed=st.number_input("Random seed",0,999999,42)
        c=st.columns(5)
        inputs=[c[i].slider(k,0,100,50) for i,k in enumerate(["Exposure","Vulnerability","Sensitivity","Adaptive capacity","Criticality"])]
        sim=monte_carlo_risk(n=n,seed=int(seed),exposure=inputs[0],vulnerability=inputs[1],sensitivity=inputs[2],adaptive_capacity=inputs[3],criticality=inputs[4])
        summ=summarize(sim); m=st.columns(5)
        m[0].metric("Mean",f"{summ['mean']:.1f}");m[1].metric("P10",f"{summ['p10']:.1f}");m[2].metric("Median",f"{summ['median']:.1f}");m[3].metric("P90",f"{summ['p90']:.1f}");m[4].metric("≥70",f"{summ['high_pct']:.1f}%")
        st.plotly_chart(px.histogram(sim,x="Risk index",nbins=35,title="Distribution of simulated risk index"),use_container_width=True)
        st.dataframe(sim.head(100),use_container_width=True,hide_index=True)

    else:
        st.subheader("River / Link Canal Network Routing")
        st.write("Use this engine for a simplified directed network of rivers, canals, barrages or transfer links.")
        st.code("from network_engine import route_network\n# links: columns from, to, capacity\n# source_inflows={...}")
        st.info("The network engine is available as network_engine.py for extension with your own river/canal topology.")

elif choice == "📊 Data Analytics & Graphs":
    st.title("Upload Data → Clean → Analyze → Graph")
    st.write("Upload one or multiple CSV, PDF, XLSX or XLS files. The application extracts the data, converts numeric fields where possible, and generates interactive Plotly graphs from the actual uploaded values.")
    st.info("PDF support covers selectable-text PDFs, table PDFs, and scanned/image PDFs when OCR is available. No unreadable values are invented.")
    files = st.file_uploader("Choose CSV, PDF or Excel files", type=["csv","pdf","xlsx","xls"], accept_multiple_files=True)
    if files:
        for uploaded in files:
            with st.expander(f"📄 {uploaded.name}", expanded=True):
                try:
                    loaded, meta = load_uploaded_file(uploaded)
                    df = coerce_numeric(loaded)
                    st.success(f"Loaded {len(df):,} rows × {len(df.columns):,} columns")
                    if meta.get("type") == "pdf":
                        st.caption(f"PDF extraction mode: {meta.get("extraction", "unknown")}")
                        for warning in meta.get("warnings", []):
                            st.warning(warning)
                    st.dataframe(df.head(200), use_container_width=True, hide_index=True)

                    # River-basin telemetry variance + optional water-quality indexes.
                    st.markdown("### 🌊 River Basin Telemetry & Water Quality Analytics")
                    basin_col = detect_basin_column(df)
                    quality_cols = detect_water_quality_columns(df)
                    telemetry_cols = detect_telemetry_columns(df, exclude=[basin_col] if basin_col else [])

                    basin_options = list(df.columns)
                    selected_basin = st.selectbox(
                        "River basin / watershed column",
                        ["Auto-detect"] + basin_options,
                        index=0,
                        key=f"basin_{uploaded.name}",
                    )
                    if selected_basin != "Auto-detect":
                        basin_col = selected_basin

                    numeric_cols = chart_candidates(df)["numeric"]
                    default_telemetry = [c for c in telemetry_cols if c in numeric_cols]
                    selected_telemetry = st.multiselect(
                        "Telemetry variables for variance analysis",
                        numeric_cols,
                        default=default_telemetry,
                        key=f"telemetry_{uploaded.name}",
                        help="Select gauge, discharge, level, flow, sensor or other numeric telemetry fields. The engine calculates sample variance within each basin and then averages the available telemetry variances.",
                    )

                    if basin_col and selected_telemetry:
                        variance_df = telemetry_variance_by_basin(df, basin_col, selected_telemetry)
                        if not variance_df.empty:
                            st.dataframe(variance_df, use_container_width=True, hide_index=True)
                            fig_var = px.bar(
                                variance_df.dropna(subset=["average_telemetry_variance"]),
                                x=basin_col, y="average_telemetry_variance",
                                title="Average Telemetry Data Variance by River Basin",
                                labels={"average_telemetry_variance": "Average telemetry variance", basin_col: "River basin"},
                            )
                            st.plotly_chart(fig_var, use_container_width=True)
                            top = variance_df.dropna(subset=["average_telemetry_variance"]).head(1)
                            if not top.empty:
                                st.success(f"Highest average telemetry variance: **{top.iloc[0][basin_col]}** ({top.iloc[0]['average_telemetry_variance']:.4g}).")
                    else:
                        st.info("To calculate basin-level telemetry variance, provide/select a river-basin column and at least one numeric telemetry variable.")

                    # Dissolved oxygen and additional water-quality indexes.
                    st.markdown("#### 🧪 Optional Water Quality Indexes")
                    detected_quality = list(quality_cols.keys())
                    selected_quality_labels = st.multiselect(
                        "Water-quality parameters",
                        detected_quality,
                        default=["Dissolved Oxygen (DO)"] if "Dissolved Oxygen (DO)" in detected_quality else detected_quality[:1],
                        key=f"quality_{uploaded.name}",
                        help="Dissolved Oxygen (DO) is included when detected. You can also analyze pH, turbidity, TDS, conductivity, temperature, nitrate, BOD, COD and coliform where present.",
                    )
                    if basin_col and selected_quality_labels:
                        selected_quality_cols = {k: quality_cols[k] for k in selected_quality_labels}
                        quality_summary = water_quality_summary(df, basin_col, selected_quality_cols)
                        if not quality_summary.empty:
                            st.dataframe(quality_summary, use_container_width=True, hide_index=True)
                            quality_metric = st.selectbox(
                                "Water-quality index to visualize",
                                selected_quality_labels,
                                key=f"quality_metric_{uploaded.name}",
                            )
                            qplot = quality_summary[[basin_col, quality_metric]].dropna()
                            if not qplot.empty:
                                fig_q = px.bar(
                                    qplot, x=basin_col, y=quality_metric,
                                    title=f"Average {quality_metric} by River Basin",
                                    labels={basin_col: "River basin", quality_metric: quality_metric},
                                )
                                st.plotly_chart(fig_q, use_container_width=True)

                    # Provide a reproducible Python visualization script based on the uploaded columns.
                    if basin_col and selected_telemetry:
                        script_quality = {k: quality_cols[k] for k in selected_quality_labels} if 'selected_quality_labels' in locals() else {}
                        script = generate_visualization_script(basin_col, selected_telemetry, script_quality)
                        with st.expander("🐍 Python visualization script", expanded=False):
                            st.code(script, language="python")
                            st.download_button(
                                "⬇️ Download Python visualization script",
                                script.encode("utf-8"),
                                f"{uploaded.name.rsplit('.',1)[0]}_river_basin_telemetry_visualization.py",
                                "text/x-python",
                                key=f"script_{uploaded.name}",
                            )

                    numeric, categorical = chart_candidates(df)
                    if numeric:
                        kind = st.selectbox("Chart", ["Bar chart","Pie chart","Scatter plot","Line chart"], key=f"kind_{uploaded.name}")
                        if kind == "Scatter plot":
                            x = st.selectbox("X numeric column", numeric, key=f"x_{uploaded.name}")
                            y = st.selectbox("Y numeric column", numeric, index=min(1,len(numeric)-1), key=f"y_{uploaded.name}")
                            fig = px.scatter(df, x=x, y=y, hover_data=categorical[:5], title=f"{y} vs {x}")
                        else:
                            metric = st.selectbox("Numeric column", numeric, key=f"metric_{uploaded.name}")
                            group = st.selectbox("Category / time column", categorical or [numeric[0]], key=f"group_{uploaded.name}")
                            if kind == "Bar chart":
                                agg = st.selectbox("Aggregation", ["sum","mean","count"], key=f"agg_{uploaded.name}")
                                if agg == "count":
                                    p = df.groupby(group, dropna=False).size().reset_index(name="count")
                                    fig = px.bar(p, x=group, y="count", title=f"Count by {group}")
                                else:
                                    p = df.groupby(group, dropna=False)[metric].agg(agg).reset_index()
                                    fig = px.bar(p, x=group, y=metric, title=f"{agg.title()} of {metric} by {group}")
                            elif kind == "Pie chart":
                                p = df.groupby(group, dropna=False)[metric].sum().reset_index()
                                fig = px.pie(p, names=group, values=metric, title=f"{metric} by {group}")
                            else:
                                fig = px.line(df, x=group, y=metric, markers=True, title=f"{metric} over {group}")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No numeric columns were detected for quantitative charts.")
                    st.download_button("⬇️ Download cleaned CSV", df.to_csv(index=False).encode(), f"{uploaded.name.rsplit('.',1)[0]}_cleaned.csv", "text/csv", key=f"dl_{uploaded.name}")
                except Exception as e:
                    st.error(f"Could not parse {uploaded.name}: {e}")
                    st.info("Text/table PDFs are supported. Image-only scanned PDFs require OCR software; the app will not invent unreadable values.")
    else:
        st.info("Upload files above to generate graphs from your own data.")

elif choice == "🧭 Regional Profiles":
    st.title("Regional Profiles & Major Cities")
    show_table(filter_df(REGIONAL_PROFILE, province, search))
    st.subheader("Major cities / service centres")
    show_table(filter_df(MAJOR_CITIES, province, search))

elif choice == "📚 Sources":
    st.title("Primary / Supporting Sources")
    for s in SOURCES:
        st.markdown(f"- [{s['title']}]({s['url']})")
    st.info("For legal, project-status and engineering claims, consult the linked primary institutional source and its current version.")

st.divider()
st.caption(f"IndusSphere Pakistan · Creator: {CREATOR} · Educational and decision-support visualization. Verify engineering, legal, environmental and statistical inputs before professional use.")
