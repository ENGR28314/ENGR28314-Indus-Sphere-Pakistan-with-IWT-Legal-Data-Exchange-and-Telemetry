"""Documented PCA/IWT timeline and attributed positions. Not legal advice."""
import pandas as pd

PCA_VALIDITY_NOTE = (
    "Pakistan's stated position is that the Court of Arbitration is a legally sound dispute-resolution body "
    "properly constituted under Article IX and Annexure G of the Indus Waters Treaty. The PCA's public case "
    "record identifies the arbitration as constituted pursuant to Annexure G and lists the case as pending. "
    "India has publicly rejected the Court's jurisdiction and described it as illegally constituted. These are "
    "competing positions; the dashboard does not resolve the dispute."
)

PCA_EVENTS = [
    {"date":"1960-09-19","event":"Indus Waters Treaty signed","category":"Treaty baseline","status":"Historical fact","source":"IWT"},
    {"date":"2016-08-19","event":"Pakistan instituted arbitral proceedings under Annexure G","category":"Arbitration","status":"PCA case record","source":"PCA Case No. 2023-01"},
    {"date":"2023-07-06","event":"Award on competence of the Court of Arbitration","category":"Arbitration","status":"PCA award","source":"PCA"},
    {"date":"2025-06-27","event":"Supplemental Award on competence","category":"Arbitration","status":"PCA award","source":"PCA"},
    {"date":"2025-08-08","event":"Award on issues of general interpretation of the IWT","category":"Arbitration","status":"PCA award","source":"PCA"},
    {"date":"2026-05-15","event":"Award concerning maximum pondage","category":"Technical interpretation","status":"PCA award","source":"PCA"},
    {"date":"2026-08-31","event":"Award on treaty status and Order on interim measures concerning Ratle","category":"Arbitration","status":"PCA award/order","source":"PCA"},
    {"date":"2027-07 (expected)","event":"Neutral Expert final technical determination referenced in public case materials","category":"Neutral Expert","status":"Expected / subject to proceedings","source":"PCA/ASIL summaries"},
]

def pca_timeline_df():
    return pd.DataFrame(PCA_EVENTS)
