import numpy as np
import pandas as pd

def peak_flow_scenario(base_flow_m3s, rainfall_multiplier=1.0, catchment_response=1.0):
    base = np.asarray(base_flow_m3s, dtype=float)
    peak = np.maximum(base, 0) * float(rainfall_multiplier) * float(catchment_response)
    return pd.DataFrame({"base_flow_m3s":base, "scenario_peak_flow_m3s":peak})

def simple_inundation_index(flow_m3s, channel_capacity_m3s):
    flow = np.asarray(flow_m3s, dtype=float)
    cap = max(float(channel_capacity_m3s), 1e-9)
    exceedance = np.maximum(flow-cap, 0)
    index = np.clip(exceedance/cap*100, 0, 100)
    return pd.DataFrame({"flow_m3s":flow, "exceedance_m3s":exceedance, "inundation_index":index})
