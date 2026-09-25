import numpy as np
import pandas as pd

def monte_carlo_risk(n=5000, exposure=50, vulnerability=50, sensitivity=50, adaptive_capacity=50, seed=42):
    rng = np.random.default_rng(seed)
    e = np.clip(rng.normal(exposure, 10, n), 0, 100)
    v = np.clip(rng.normal(vulnerability, 10, n), 0, 100)
    s = np.clip(rng.normal(sensitivity, 10, n), 0, 100)
    a = np.clip(rng.normal(adaptive_capacity, 10, n), 0, 100)
    risk = np.clip(0.30*e + 0.30*v + 0.25*s + 0.15*(100-a), 0, 100)
    return pd.DataFrame({"exposure":e,"vulnerability":v,"sensitivity":s,"adaptive_capacity":a,"risk":risk})

def summarize(results):
    return results["risk"].describe(percentiles=[.05,.25,.5,.75,.95]).to_frame("risk")
