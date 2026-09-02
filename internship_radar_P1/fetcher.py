import requests

# ============================================================
#   🌐 DATA SOURCE - Remotive API (REAL remote jobs)
# ============================================================

API_URL = "https://remotive.com/api/remote-jobs"

def is_open_to_india(location):
    """Kya job India/worldwide ke liye open hai?"""
    loc = location.lower()
    # Worldwide/anywhere/global jobs = India se apply kar sakte hain
    open_keywords = ["world", "anywhere", "global", "remote"]
    return any(word in loc for word in open_keywords)

def fetch_remote_jobs(limit=100):
    """INTERNET se REAL remote jobs fetch karo"""
    print("🌐 Internet se REAL jobs fetch ho rahi hain...")

    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API error: {e}")
        return []

    jobs = data.get("jobs", [])
    print(f"📥 API se total {len(jobs)} jobs aayi")

    internships = []
    for job in jobs:
        location = job.get("location", "Remote")

        # Sirf worldwide/India-open jobs rakho
        if not is_open_to_india(location):
            continue

        # Tags ko skills list mein convert karo
        skills = [tag.lower().strip() for tag in job.get("tags", [])]

        internships.append({
            "title": job.get("title", "N/A"),
            "company": job.get("company", "N/A"),
            "location": location,
            "mode": "wfh",              # Remotive ki sab jobs remote hain
            "stipend": job.get("salary", "") or "Negotiable",
            "duration": "Remote Job",
            "posted": job.get("publication_date", "")[:10],
            "skills": skills,
        })

        if len(internships) >= limit:
            break

    print(f"✅ {len(internships)} worldwide remote jobs filter hui")
    return internships