import pandas as pd
import os

SEEN_FILE = "seen_jobs.csv"

def load_seen():
    """Pehle dekhi hui job IDs load karo"""
    if os.path.exists(SEEN_FILE):
        df = pd.read_csv(SEEN_FILE)
        return set(df["job_id"].tolist())
    return set()   # pehli baar hai, kuch nahi dekha

def filter_new(candidates, seen_ids):
    """Sirf NAYI jobs return karo (jo pehle nahi dekhi)"""
    return [c for c in candidates if c["id"] not in seen_ids]

def update_seen(new_candidates, seen_ids):
    """Nayi jobs ko 'seen' list mein daalo + save karo"""
    for c in new_candidates:
        seen_ids.add(c["id"])
    pd.DataFrame({"job_id": list(seen_ids)}).to_csv(SEEN_FILE, index=False)