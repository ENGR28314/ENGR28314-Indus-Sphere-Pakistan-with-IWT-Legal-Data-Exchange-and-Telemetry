"""Neutral timeline engine for documented IWT events."""
import pandas as pd

DEFAULT_EVENTS = [
    {"date":"1960-09-19","event":"Indus Waters Treaty signed","category":"Treaty baseline","source":"Treaty text"},
    {"date":"2022-05-30","event":"PIC meeting in New Delhi referenced in supplied material","category":"PIC practice","source":"User-provided material; verify against official record"},
    {"date":"2025-04-23","event":"India announced decision to hold IWT in abeyance","category":"Treaty status","source":"Government of India public statements"},
    {"date":"2025-06-27","event":"PCA Supplemental Award on competence","category":"Arbitration","source":"PCA"},
    {"date":"2025-08-08","event":"PCA Award on issues of general interpretation","category":"Arbitration","source":"PCA"},
    {"date":"2026-05-15","event":"PCA award concerning maximum pondage","category":"Arbitration","source":"PCA"},
    {"date":"2026-08-31","event":"PCA Award on treaty status and Order on interim measures","category":"Arbitration","source":"PCA"},
]

def timeline_df():
    return pd.DataFrame(DEFAULT_EVENTS)
