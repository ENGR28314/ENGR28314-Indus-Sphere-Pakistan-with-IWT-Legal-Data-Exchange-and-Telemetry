"""Neutral, source-attributed data for India-side Indus basin projects and Pakistan's stated concerns."""
import pandas as pd

INDIA_PROJECTS = pd.DataFrame([
    {"item":"113-km inter-basin canal proposal","category":"Canal / inter-basin transfer","details":"NDTV reported a feasibility-stage proposal for a 113 km canal linking the Chenab with the Ravi-Beas-Sutlej system, with potential onward distribution to Punjab, Haryana and Rajasthan.","status":"Feasibility / preliminary reporting","source":"NDTV, 16 Jun 2025"},
    {"item":"Ravi-Beas link proposal","category":"Canal / inter-basin transfer","details":"Reported proposals include additional canal connectivity intended to improve use of waters in the Ravi-Beas-Sutlej system; project scope and implementation should be verified against current official planning documents.","status":"Reported proposal","source":"NDTV / related reporting"},
    {"item":"Pakal Dul","category":"Hydropower","details":"1,000 MW project in the Chenab basin; India's Ministry of Power reported a target to commission it by December 2026 in January 2026.","status":"Under construction / official target","source":"Government of India Ministry of Power"},
    {"item":"Ratle","category":"Hydropower","details":"850 MW-class Chenab basin project central to the current IWT technical proceedings and interim-measures order.","status":"Under construction / subject to proceedings","source":"PCA / project records"},
    {"item":"Kiru","category":"Hydropower","details":"624 MW project in the Chenab basin; India's Ministry of Power reported a target to commission it by December 2026 in January 2026.","status":"Under construction / official target","source":"Government of India Ministry of Power"},
    {"item":"Kwar","category":"Hydropower","details":"540 MW project in the Chenab basin; India's Ministry of Power reported a target for March 2028 in January 2026.","status":"Under construction / official target","source":"Government of India Ministry of Power"},
])

DISPUTED_ENGINEERING = pd.DataFrame([
    {"metric":"Pondage / live storage","project":"Kishanganga","description":"The parties have disputed the permissible maximum pondage and its engineering implications under Annexure D."},
    {"metric":"Pondage / live storage","project":"Ratle","description":"The parties have disputed the permissible maximum pondage and its engineering implications under Annexure D."},
    {"metric":"Spillway configuration","project":"Kishanganga / Ratle","description":"The proceedings address design components of run-of-river plants, including spillway configuration and related hydraulic effects."},
    {"metric":"Intake / outlet elevations","project":"Kishanganga / Ratle","description":"The proceedings address elevations and design components that affect operation of run-of-river plants."},
    {"metric":"Freeboard / design elevation","project":"Ratle","description":"Freeboard and other design components have been considered in the treaty interpretation proceedings."},
])

PAKISTAN_POSITION = [
    "Pakistan has argued in the proceedings that certain Indian project designs must comply with the treaty's technical limits for run-of-river hydro-electric plants.",
    "Pakistan has sought interim measures concerning construction at Ratle while the parallel Neutral Expert process addresses technical questions.",
    "Claims about deliberate manipulation of flows, droughts or floods are presented here as attributed positions rather than as established facts."
]

def projects_df(): return INDIA_PROJECTS.copy()
def engineering_df(): return DISPUTED_ENGINEERING.copy()
