# Add these imports to your existing IndusSphere Pakistan app.py.
from agro_economic import render_agro_economic
from socio_economic import render_socio_economic
from simulation_dashboard import render_simulation_dashboard
from dispute_tab import render_dispute_tab
from park_maps import render_park_details

# Example tab wiring:
# tab_agro, tab_socio, tab_sim, tab_dispute = st.tabs([
#     "Agro-Economic", "Socio-Economic", "Engineering Simulations",
#     "India-related water infrastructure & IWT dispute"
# ])
#
# with tab_agro:
#     render_agro_economic()
# with tab_socio:
#     render_socio_economic()
# with tab_sim:
#     render_simulation_dashboard()
# with tab_dispute:
#     render_dispute_tab()
#
# In the existing Parks Details section, pass your existing parks dataframe:
# render_park_details(parks_df)
#
# Required park dataframe columns:
# name, latitude, longitude
# Optional:
# radius_m
