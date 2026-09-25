from datetime import date

def event(title, when, category, description, source="", status="Documented"):
    return {"title":title,"date":when,"category":category,"description":description,"source":source,"status":status}

def sort_events(events):
    return sorted(events, key=lambda x: str(x["date"]))
