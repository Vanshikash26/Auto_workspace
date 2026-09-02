import config
import fetcher 

# ============================================================
#   🎯 INTERNSHIP RADAR - MATCHING ENGINE
# ============================================================

# Skill aliases (alag naam, same skill)
SKILL_ALIASES = {
    "js": "javascript",
    "gzb": "ghaziabad",
    "scraping": "web scraping",
    "rest": "rest api",
    "rest-api": "rest api",
    "restful": "rest api",
    "postgres": "sql",
    "postgresql": "sql",
}

def normalize_skill(skill):
    """Skill ko lowercase + alias resolve karo"""
    skill = skill.lower().strip()
    return SKILL_ALIASES.get(skill, skill)

def normalize_city(city):
    """City ko lowercase + alias resolve karo"""
    city = city.lower().strip()
    return {"gzb": "ghaziabad"}.get(city, city)

# Config se skills load karo (normalized)
CORE_SKILLS = {normalize_skill(s) for s in config.MY_SKILLS["core"]}
KNOWN_SKILLS = {normalize_skill(s) for s in config.MY_SKILLS["known"]}
TARGET_CITIES = {normalize_city(c) for c in config.TARGET_CITIES}

# ============================================================
#   MATCHING FUNCTIONS
# ============================================================

def calculate_skill_score(internship_skills):
    """Kitni skills match hui + score nikalo"""
    score = 0
    matched_core = []
    matched_known = []

    for skill in internship_skills:
        s = normalize_skill(skill)
        if s in CORE_SKILLS:
            score += config.CORE_SKILL_WEIGHT
            matched_core.append(skill)
        elif s in KNOWN_SKILLS:
            score += config.KNOWN_SKILL_WEIGHT
            matched_known.append(skill)

    return score, matched_core, matched_known

def is_location_ok(internship):
    """Kya location acceptable hai? WFH hamesha OK"""
    if internship["mode"].lower() == "wfh":
        return True
    city = normalize_city(internship["location"])
    return any(t in city or city in t for t in TARGET_CITIES)

def calculate_total_score(internship):
    """Overall score + details nikalo"""
    skill_score, matched_core, matched_known = calculate_skill_score(internship["skills"])

    if internship["mode"].lower() == "wfh":
        mode_bonus = config.WFH_BONUS
        mode_label = "🏠 WFH"
    else:
        mode_bonus = config.OFFICE_BONUS
        mode_label = "🏢 Office"

    return {
        "total": skill_score + mode_bonus,
        "skill_score": skill_score,
        "matched_core": matched_core,
        "matched_known": matched_known,
        "mode_label": mode_label,
    }

# ============================================================
#   DISPLAY FUNCTIONS
# ============================================================

def display_header():
    print("\n" + "=" * 60)
    print("🎯  I N T E R N S H I P   R A D A R")
    print("=" * 60)
    print(f"   🛠️  Core Skills : {', '.join(config.MY_SKILLS['core'])}")
    print(f"   📚 Known Skills : {', '.join(config.MY_SKILLS['known'])}")
    print(f"   📍 Cities       : {', '.join(config.TARGET_CITIES)} (ya WFH)")
    print("=" * 60)

def display_internship(rank, intern, details):
    print(f"\n{'─' * 60}")
    print(f"  #{rank}  {intern['title']}")
    print(f"  🏛️  {intern['company']}")
    print(f"  {details['mode_label']} | 📍 {intern['location']}")
    print(f"  💰 ₹{intern['stipend']}/month | ⏱️  {intern['duration']} | 📅 {intern['posted']}")

    if details["matched_core"]:
        print(f"  ⭐ Core Matched  : {', '.join(details['matched_core'])}")
    if details["matched_known"]:
        print(f"  📘 Known Matched : {', '.join(details['matched_known'])}")

    print(f"  📊 Match Score   : {details['total']}")

# ============================================================
#   SAMPLE DATA (Part 2 mein REAL scraping se aayega)
# ============================================================

def get_sample_internships():
    return [
        {"title": "Python Developer Intern", "company": "TechNova Solutions",
         "location": "Delhi", "mode": "wfh", "stipend": "10000",
         "duration": "3 months", "posted": "2 days ago",
         "skills": ["python", "sql", "rest api"]},

        {"title": "Web Scraping Intern", "company": "DataHarvest Analytics",
         "location": "Noida", "mode": "office", "stipend": "8000",
         "duration": "2 months", "posted": "1 day ago",
         "skills": ["python", "web scraping", "sql"]},

        {"title": "Java Developer Intern", "company": "FinEdge Technologies",
         "location": "Delhi", "mode": "office", "stipend": "12000",
         "duration": "6 months", "posted": "3 days ago",
         "skills": ["java", "mysql", "sql"]},

        {"title": "Frontend Developer Intern", "company": "PixelCraft Studio",
         "location": "Gurgaon", "mode": "office", "stipend": "9000",
         "duration": "3 months", "posted": "1 day ago",
         "skills": ["html", "css", "js"]},

        {"title": "Data Analyst Intern", "company": "InsightHub",
         "location": "Bangalore", "mode": "office", "stipend": "15000",
         "duration": "4 months", "posted": "5 days ago",
         "skills": ["sql", "python"]},

        {"title": "Backend Developer Intern", "company": "CloudSprint",
         "location": "Ghaziabad", "mode": "office", "stipend": "11000",
         "duration": "3 months", "posted": "2 days ago",
         "skills": ["java", "rest api", "mysql"]},

        {"title": "Full Stack Intern", "company": "StackForge",
         "location": "Noida", "mode": "office", "stipend": "16000",
         "duration": "6 months", "posted": "1 day ago",
         "skills": ["python", "js", "html", "css", "sql"]},

        {"title": "QA Automation Intern", "company": "TestPro",
         "location": "Delhi", "mode": "wfh", "stipend": "8500",
         "duration": "2 months", "posted": "4 days ago",
         "skills": ["python", "sql", "selenium"]},

        {"title": "Android Developer Intern", "company": "Appify",
         "location": "Delhi", "mode": "office", "stipend": "10000",
         "duration": "3 months", "posted": "2 days ago",
         "skills": ["kotlin", "android"]},

        {"title": "ML Intern", "company": "NeuroLab AI",
         "location": "Delhi", "mode": "wfh", "stipend": "14000",
         "duration": "4 months", "posted": "1 day ago",
         "skills": ["python", "tensorflow"]},

        {"title": "DevOps Intern", "company": "InfraCore",
         "location": "Pune", "mode": "office", "stipend": "13000",
         "duration": "3 months", "posted": "3 days ago",
         "skills": ["docker", "kubernetes"]},

        {"title": "Database Intern", "company": "DataVault",
         "location": "Ghaziabad", "mode": "office", "stipend": "9500",
         "duration": "2 months", "posted": "1 day ago",
         "skills": ["mysql", "sql"]},

        {"title": "API Developer Intern", "company": "ConnectAPI",
         "location": "Noida", "mode": "wfh", "stipend": "12000",
         "duration": "3 months", "posted": "2 days ago",
         "skills": ["python", "rest api", "sql"]},
    ]

# ============================================================
#   MAIN FUNCTION
# ============================================================

def main():
    display_header()

        # REAL data fetch karo (API se)
    internships = fetcher.fetch_remote_jobs(limit=100)

    # Agar API fail ho, toh sample data use karo (fallback)
    if not internships:
        print("⚠️ Real data nahi mila, sample data use kar rahe hain")
        internships = get_sample_internships()

    candidates = []
    rejected_location = 0
    rejected_skills = 0

    for intern in internships:
        # Filter 1: Location
        if not is_location_ok(intern):
            rejected_location += 1
            continue

        # Filter 2: Skill score
        details = calculate_total_score(intern)
        if details["skill_score"] < config.MIN_SKILL_SCORE:
            rejected_skills += 1
            continue

        candidates.append((details["total"], intern, details))

    # Best score sabse upar
    candidates.sort(key=lambda x: x[0], reverse=True)

    print(f"\n✅ {len(candidates)} internships MATCH hui!")
    print(f"🚫 Rejected: {rejected_location} (location), {rejected_skills} (skills)")

        # Top 10 hi dikhao
    for rank, (score, intern, details) in enumerate(candidates[:10], 1):
        display_internship(rank, intern, details)

    print(f"\n{'=' * 60}")
    if candidates:
        top = candidates[0][1]
        print(f"🏆 TOP PICK: {top['title']} @ {top['company']}")
    print("=" * 60)

if __name__ == "__main__":
    main()