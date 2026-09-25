import numpy as np
import pandas as pd

SCENARIOS = {
    "Low": {"temperature_delta_c": 0.8, "precipitation_delta_pct": 2},
    "Moderate": {"temperature_delta_c": 1.8, "precipitation_delta_pct": 0},
    "High": {"temperature_delta_c": 3.0, "precipitation_delta_pct": -5},
}

def apply_climate_scenario(df, scenario, temperature_col="temperature_c", precipitation_col="precipitation_mm"):
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")
    out = df.copy()
    p = SCENARIOS[scenario]
    if temperature_col in out:
        out["scenario_temperature_c"] = pd.to_numeric(out[temperature_col], errors="coerce") + p["temperature_delta_c"]
    if precipitation_col in out:
        out["scenario_precipitation_mm"] = pd.to_numeric(out[precipitation_col], errors="coerce") * (1+p["precipitation_delta_pct"]/100)
    return out
