# IndusSphere Pakistan — Water, Terrain, Climate & Strategic Explorer

**Creator: Engr. Syed Hassan Iqbal Shah**

A Pakistan Water/Terrain Explorer-style Streamlit dashboard with sidebar navigation, curated Pakistan water/terrain inventories, interactive scenario inputs, socio-economic and agro-economic analysis, and user-data analytics.

## User-data analytics
Upload one or multiple:
- CSV
- PDF (selectable text/table)
- PDF (scanned/image; OCR fallback when Tesseract is available)
- XLSX
- XLS

The app analyzes the actual uploaded data and can generate:
- Bar charts
- Pie charts
- Scatter plots
- Line charts

It also supports numeric conversion, category grouping, aggregation, data preview, and cleaned CSV download.

## Socio-economic & agro-economic
Includes:
- Population, employment, poverty/income, urban growth, food security, tourism, utilities, energy and climate vulnerability
- IBIS/agriculture context
- **Kharif** season and crop types
- **Rabi** season and crop types
- Crop production and cultivated-area inputs
- **Apiculture**: colonies, honey, beeswax, pollination and planning indicators
- **Aquaculture**: pond/tank production, stocking, feed, survival, harvest and water-quality indicators
- Editable province/region dataset whose graphs update from the values entered by the user

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

For Streamlit Community Cloud, `packages.txt` installs Tesseract OCR so scanned PDFs can use the OCR fallback. OCR quality depends on scan quality and language availability.

## Important
The dashboard is an educational/decision-support visualization. Curated geographic and engineering information should be verified against authoritative datasets before professional use. Uploaded data are analyzed as supplied; the app does not manufacture missing observations.

## Simulation engines

The project now includes modular, input-driven simulation engines:

- `hydrology_engine.py` — reservoir mass balance, storage trajectory, demand shortage and spill screening.
- `flood_engine.py` — rainfall-runoff, channel-capacity exceedance and rainfall sensitivity screening.
- `crop_water_engine.py` — Rabi/Kharif crop water requirement and irrigation-volume screening.
- `climate_engine.py` — baseline/medium/worst-case climate stress and parameter sensitivity analysis.
- `monte_carlo_engine.py` — uncertainty simulation and percentile/risk-distribution analysis.
- `network_engine.py` — simplified directed river/link-canal routing using capacities and losses.
- `simulation_engine.py` — common engine registry/import layer used by the Streamlit interface.

These engines are screening/educational models. They are not calibrated replacements for HEC-RAS, SWAT, WEAP, MIKE, MODFLOW, EPANET, or project-specific hydrologic/hydraulic design models. Inputs, equations and assumptions should be calibrated and validated before engineering use.

## September 2026 extension

This build adds:
- Detailed Rabi/Kharif crop tables with season, crop, typical window and engineering water notes.
- Structured Apiculture and Aquaculture indicators.
- Fully input-driven socio/agro analytics with Bar, Pie, Scatter and Line charts and the requested five metrics.
- Park-detail maps in the “Select a park for details” view using representative coordinates.
- PCA/IWT validity-position timeline with primary-source attribution and a neutral presentation of competing legal positions.
- “Indian Atrocities” research tab (requested label) covering reported inter-basin canal proposals, Chenab hydropower projects, disputed engineering specifications and Neutral Expert timing, with claims attributed rather than treated as independent conclusions.
- Additional Python simulation modules: `simulation_runner.py` and `engineering_simulations.py`, alongside hydrology, flood, crop-water, climate, Monte Carlo and river/canal network engines.

The application remains input-driven and does not use these datasets as immutable final risk outputs. Engineering simulations are screening/educational models and should be calibrated and validated before professional design use.
