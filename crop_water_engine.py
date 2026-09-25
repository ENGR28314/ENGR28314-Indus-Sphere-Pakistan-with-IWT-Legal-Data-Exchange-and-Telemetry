import numpy as np
import pandas as pd

def crop_water_requirement(eto_mm, kc_values, effective_rain_mm=0, efficiency=0.65):
    eto = np.asarray(eto_mm, dtype=float)
    kc = np.asarray(kc_values, dtype=float)
    rain = np.asarray(effective_rain_mm, dtype=float)
    etc = eto * kc
    net = np.maximum(etc - rain, 0)
    gross = net / max(float(efficiency), 1e-9)
    return pd.DataFrame({"ETo_mm":eto, "Kc":kc, "ETc_mm":etc, "EffectiveRain_mm":rain,
                         "NetIrrigation_mm":net, "GrossIrrigation_mm":gross})

def seasonal_water_scenario(base_requirement_mm, rainfall_change_pct=0, efficiency=0.65):
    adjusted = np.asarray(base_requirement_mm, dtype=float) * (1 + rainfall_change_pct/100)
    return adjusted / max(float(efficiency), 1e-9)
