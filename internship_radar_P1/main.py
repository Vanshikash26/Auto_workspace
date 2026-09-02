import config
import fetcher
import state
import notifier
import reporter 

# ============================================================
#   SKILL MATCHING (Part 1 wala logic)
# ============================================================
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
    skill = skill.lower().strip()
    return SKILL_ALIASES.get(skill, skill)

def normalize_city(city):
    city = city.lower().strip()
    return {"gzb": "ghaziabad"}.get(city, city)

CORE_SKILLS = {normalize_skill(s) for s in config.MY_SKILLS["core"]}
KNOWN_SKILLS = {normalize_skill(s) for s in config.MY_SKILLS["known"]}
TARGET_CITIES = {normalize_city(c) for c in config.TARGET_CITIES}

def calculate_skill_score(internship_skills):
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
    if internship["mode"].lower() == "wfh":
        return True
    city = normalize_city(internship["location"])
    return any(t in city or city in t for t in TARGET_CITIES)

def calculate_total_score(internship):
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
#   DISPLAY
# ============================================================
def display_header():
    print("\n" + "=" * 60)
    print("🎯  I N T E R N S H I P   R A D A R")
    print("=" * 60)
    print(f"   🛠️  Core Skills : {', '.join(config.MY_SKILLS['core'])}")
    print(f"   📚 Known Skills : {', '.join(config.MY_SKILLS['known'])}")
    print(f"   📍 Cities       : {', '.join(config.TARGET_CITIES)} (ya WFH)")
    print("=" * 60)

def display_internship(rank, c):
    print(f"\n{'─' * 60}")
    print(f"  #{rank}  {c['title']}")
    print(f"  🏛️  {c['company']}")
    print(f"  {c['mode_label']} | 📍 {c['location']}")
    print(f"  💰 {c['stipend']} | ⏱️  {c['duration']} | 📅 {c['posted']}")
    if c["matched_core"]:
        print(f"  ⭐ Core Matched  : {', '.join(c['matched_core'])}")
    if c["matched_known"]:
        print(f"  📘 Known Matched : {', '.join(c['matched_known'])}")
    print(f"  📊 Match Score   : {c['total']}")
    print(f"  🔗 Apply Here    : {c['url']}")

# ============================================================
#   MAIN
# ============================================================
def main():
    display_header()

    # Step 1: REAL jobs fetch karo
    jobs = fetcher.fetch_remote_jobs(limit=100)
    if not jobs:
        print("⚠️ Real data nahi mila, is baar kuch nahi dikha sakte")
        return

    # Step 2: Match + Score karo
    candidates = []
    rejected_location = 0
    rejected_skills = 0

    for job in jobs:
        if not is_location_ok(job):
            rejected_location += 1
            continue
        details = calculate_total_score(job)
        if details["skill_score"] < config.MIN_SKILL_SCORE:
            rejected_skills += 1
            continue
        # Job + details ko merge karo
        candidate = {**job, **details}
        candidates.append(candidate)

    # Best score sabse upar
    candidates.sort(key=lambda x: x["total"], reverse=True)

    # Step 3: STATE - Sirf NAYI jobs nikalo
    seen_ids = state.load_seen()
    new_candidates = state.filter_new(candidates, seen_ids)

    print(f"\n📊 Total matched   : {len(candidates)}")
    print(f"👀 Pehle dekh chuke: {len(candidates) - len(new_candidates)}")
    print(f"🆕 NAYI jobs       : {len(new_candidates)}")

    # Step 4: Nayi jobs dikhao + alert bhejo
    if new_candidates:
        print(f"\n{'=' * 60}")
        print(f"🎉 {len(new_candidates)} NAYI jobs mili!")
        for rank, c in enumerate(new_candidates[:10], 1):
            display_internship(rank, c)

        # Email alert (agar enabled hai)
        notifier.send_email_alert(new_candidates)

        # Seen list update karo
        state.update_seen(new_candidates, seen_ids)
    else:
        print("\n😴 Koi nayi job nahi (sab pehle dekh chuke)")

    # Excel report banao (har baar)
    reporter.generate_report(candidates, new_candidates)

    print(f"\n{'=' * 60}")

if __name__ == "__main__":
    main()