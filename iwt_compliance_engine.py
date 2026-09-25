import pandas as pd

def compare_designs(proposed, reference):
    rows = []
    for metric, proposed_value in proposed.items():
        reference_value = reference.get(metric)
        if reference_value is None:
            rows.append({"metric":metric,"proposed":proposed_value,"reference":None,"status":"Not assessed"})
            continue
        status = "Within reference" if float(proposed_value) <= float(reference_value) else "Above reference"
        rows.append({"metric":metric,"proposed":proposed_value,"reference":reference_value,"status":status})
    return pd.DataFrame(rows)

def treaty_engineering_metrics():
    return pd.DataFrame([
        ["Pondage","Maximum pondage / firm-power calculation","Annexure D"],
        ["Spillways","Gated spillway design","Annexure D"],
        ["Intakes","Power intake design","Annexure D"],
        ["Freeboard","Safety-related freeboard","Annexure D"],
        ["Outlets","Outlets below Dead Storage Level","Annexure D"],
    ], columns=["metric","engineering_question","treaty_reference"])
