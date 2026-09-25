# IndusSphere Pakistan – Enhancement Pack

This pack extends the existing application without replacing its existing tabs, calculations, inputs, maps, exports or datasets.

## Added modules

- `agro_economic.py` — Rabi/Kharif, crop windows, engineering water notes, apiculture, aquaculture and input-driven charts.
- `socio_economic.py` — province/region socio/agro data editor, CSV/XLS/XLSX upload and Bar/Pie/Scatter/Line charts.
- `park_maps.py` — selected-park interactive Folium map.
- `simulation_dashboard.py` — Streamlit controls for engineering simulation engines.
- `hydrology_engine.py` — rainfall-runoff and reservoir balance functions.
- `crop_water_engine.py` — crop evapotranspiration and irrigation requirement functions.
- `flood_engine.py` — peak-flow and simple inundation-index scenarios.
- `climate_scenario_engine.py` — Low/Moderate/High scenario transformation.
- `monte_carlo_engine.py` — input-driven uncertainty/risk simulation.
- `network_flow_engine.py` — directed water-network maximum-flow simulation.
- `iwt_compliance_engine.py` — engineering-metric comparison utilities; it does not decide legal compliance.
- `timeline_engine.py` and `iwt_dispute_data.py` — source-aware IWT/PCA timeline data.
- `dispute_tab.py` — neutral, source-aware India-related infrastructure/IWT dispute tab.
- `app_integration_snippet.py` — exact import/tab wiring pattern.

## Park maps

The map function uses the park selected by the user. It does not use a static map image. Your existing park dataset must contain:

`name, latitude, longitude`

Optional `radius_m` draws a circle around the park.

## Political/legal content

The application should distinguish:
1. documented institutional facts;
2. Pakistan's stated position;
3. India's stated position;
4. third-party analysis;
5. user-supplied claims that have not been independently verified.

The requested tab title `indian atrocities` is therefore represented by the neutral UI label:
`India-related water infrastructure & IWT dispute`.

## Sources

Primary references used for the legal/timeline scaffolding include the Permanent Court of Arbitration case page and World Bank material on the IWT mechanisms and appointments. The PCA case page lists the 31 August 2026 award on treaty status and the 31 August 2026 order on interim measures concerning Ratle.

The 113-km canal claim and exact numerical engineering figures supplied by the user are not inserted as adjudicated facts. They should be displayed only as attributed proposals/claims with a source field if the user provides or the application retrieves a primary source.
