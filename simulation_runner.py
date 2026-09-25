"""Unified simulation registry and lightweight runner for IndusSphere."""
from hydrology_engine import monthly_water_balance
from flood_engine import flood_scenario, rainfall_sweep
from crop_water_engine import crop_water_requirement, crop_comparison
from climate_engine import climate_stress, sensitivity_table
from monte_carlo_engine import monte_carlo_risk, summarize
from network_engine import route_network

ENGINE_REGISTRY = {
    "Reservoir / Water Balance": {"module":"hydrology_engine.py","kind":"hydrology","description":"Mass-balance simulation for inflow, demand, storage, evaporation and shortage."},
    "Flood Screening": {"module":"flood_engine.py","kind":"flood","description":"Input-driven rainfall/flood screening and rainfall sensitivity sweep."},
    "Crop Water Requirement": {"module":"crop_water_engine.py","kind":"crop","description":"Crop water requirement and crop comparison calculations."},
    "Climate Stress": {"module":"climate_engine.py","kind":"climate","description":"Climate-stress and sensitivity calculations."},
    "Monte Carlo Risk": {"module":"monte_carlo_engine.py","kind":"uncertainty","description":"Probabilistic screening around user-specified risk inputs."},
    "River / Canal Network": {"module":"network_engine.py","kind":"network","description":"Flow routing through a directed river/canal network with capacity and losses."},
}

def list_engines(): return ENGINE_REGISTRY.copy()
