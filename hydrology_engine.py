import numpy as np
import pandas as pd

def rainfall_runoff_simulation(rainfall_mm, catchment_km2, runoff_coefficient=0.35, time_step_days=1):
    rainfall = np.asarray(rainfall_mm, dtype=float)
    runoff_mm = np.maximum(rainfall, 0) * float(runoff_coefficient)
    volume_m3 = runoff_mm / 1000.0 * float(catchment_km2) * 1_000_000
    return pd.DataFrame({
        "rainfall_mm": rainfall,
        "runoff_mm": runoff_mm,
        "runoff_volume_m3": volume_m3,
    })

def reservoir_balance(inflow_m3, demand_m3, initial_storage_m3, capacity_m3, release_priority="demand"):
    inflow = np.asarray(inflow_m3, dtype=float)
    demand = np.asarray(demand_m3, dtype=float)
    storage = float(initial_storage_m3)
    rows = []
    for i, (qin, qd) in enumerate(zip(inflow, demand)):
        available = storage + max(qin, 0)
        release = min(available, max(qd, 0)) if release_priority == "demand" else min(available, max(qin, 0))
        storage = min(float(capacity_m3), max(0.0, available - release))
        spill = max(0.0, available - release - float(capacity_m3))
        rows.append((i, qin, qd, release, storage, spill))
    return pd.DataFrame(rows, columns=["step","inflow_m3","demand_m3","release_m3","storage_m3","spill_m3"])
