# ========================================================
#   🎯 INTERNSHIP MATCHER - Tumhari Preferences
# ========================================================

# --- CONFIG: YE TUMHARI PREFERENCES HAIN (edit kar sakti ho) ---
MY_SKILLS = ["java", "python", "web scraping", "sql", "html", "js",
             "css", "mysql", "rest api"]

TARGET_CITIES = ["delhi", "ghaziabad", "noida"]

# Priority: Option A = WFH first, office in target cities also OK
WFH_BONUS = 15      # WFH ko extra points
OFFICE_BONUS = 8    # Target city office ko points
SKILL_WEIGHT = 10   # Har matching skill ke points


# --- SMART MATCHING: aliases handle karo ---
SKILL_ALIASES = {
    "js": "javascript",
    "gzb": "ghaziabad",
}

def normalize_skill(skill):
    skill = skill.lower().strip()
    return SKILL_ALIASES.get(skill, skill)

def normalize_city(city):
    city = city.lower().strip()
    return {"gzb": "ghaziabad"}.get(city, city)


# ========================================================
#   📋 INTERNSHIP DATA
#   (Ye real internship listings ka FORMAT hai.
#    Abhi sample data hai — aage iski jagah REAL data source plug karenge)
# ========================================================
internships = [
    {"title": "Python Developer Intern", "company": "TechNova Solutions",
     "location": "Delhi", "mode": "wfh", "stipend": "₹10,000/month",
     "skills": ["python", "sql", "rest api"]},

    {"title": "Web Scraping Intern", "company": "DataHarvest Analytics",
     "location": "Noida", "mode": "office", "stipend": "₹8,000/month",
     "skills": ["python", "web scraping", "sql"]},

    {"title": "Java Developer Intern", "company": "FinEdge Technologies",
     "location": "Delhi", "mode": "office", "stipend": "₹12,000/month",
     "skills": ["java", "mysql", "sql"]},

    {"title": "Frontend Developer Intern", "company": "PixelCraft Studio",
     "location": "Gurgaon", "mode": "office", "stipend": "₹9,000/month",
     "skills": ["html", "css", "js"]},

    {"title": "Data Analyst Intern", "company": "InsightHub",
     "location": "Bangalore", "mode": "office", "stipend": "₹15,000/month",
     "skills": ["sql", "python"]},

    {"title": "Backend Developer Intern", "company": "CloudSprint",
     "location": "Ghaziabad", "mode": "office", "stipend": "₹11,000/month",
     "skills": ["java", "rest api", "mysql"]},

    {"title": "Machine Learning Intern", "company": "NeuroLab AI",
     "location": "Delhi", "mode": "wfh", "stipend": "₹14,000/month",
     "skills": ["python", "tensorflow", "pytorch"]},

    {"title": "React Developer Intern", "company": "WebWiz",
     "location": "Noida", "mode": "office", "stipend": "₹9,500/month",
     "skills": ["react", "javascript", "css"]},

    {"title": "Android Developer Intern", "company": "Appify",
     "location": "Delhi", "mode": "office", "stipend": "₹10,000/month",
     "skills": ["kotlin", "android"]},

    {"title": "QA Automation Intern", "company": "TestPro",
     "location": "Delhi", "mode": "wfh", "stipend": "₹8,500/month",
     "skills": ["python", "selenium", "sql"]},

    {"title": "DevOps Intern", "company": "InfraCore",
     "location": "Pune", "mode": "office", "stipend": "₹13,000/month",
     "skills": ["docker", "kubernetes"]},

    {"title": "Full Stack Intern", "company": "StackForge",
     "location": "Noida", "mode": "office", "stipend": "₹16,000/month",
     "skills": ["python", "js", "html", "css", "sql", "mysql"]},
]


# ========================================================
#   🧠 MATCHING ENGINE (Asli Logic)
# ========================================================

def skill_match(internship):
    """Kitni skills match karti hain - returns (matched_skills, count)"""
    my = {normalize_skill(s) for s in MY_SKILLS}
    required = {normalize_skill(s) for s in internship["skills"]}
    matched = my & required   # intersection - common skills
    return matched, len(matched)


def location_ok(internship):
    """Kya location acceptable hai? WFH hamesha OK, office sirf target cities"""
    if internship["mode"] == "wfh":
        return True   # WFH = location matter nahi karti
    city = normalize_city(internship["location"])
    targets = {normalize_city(c) for c in TARGET_CITIES}
    # Partial match bhi allow karo (e.g., "New Delhi" matches "delhi")
    return any(t in city or city in t for t in targets)


def score(internship):
    """Overall score - skills + mode/location bonus"""
    matched, count = skill_match(internship)
    s = count * SKILL_WEIGHT
    if internship["mode"] == "wfh":
        s += WFH_BONUS
    elif internship["mode"] == "office":
        s += OFFICE_BONUS
    return s


# ========================================================
#   🔍 FILTER + RANK
# ========================================================
candidates = []
rejected = []

for intern in internships:
    if not location_ok(intern):
        rejected.append((intern, "❌ Location/City match nahi"))
        continue
    matched, count = skill_match(intern)
    if count == 0:
        rejected.append((intern, "❌ Koi skill match nahi"))
        continue
    candidates.append((score(intern), intern, matched))

# Score ke hisaab se best se worst sort karo
candidates.sort(key=lambda x: x[0], reverse=True)


# ========================================================
#   📤 OUTPUT - Tumhare Results
# ========================================================
print("=" * 55)
print("🎯 TUMHARI PREFERENCES")
print("=" * 55)
print(f"   🛠️  Skills   : {', '.join(MY_SKILLS)}")
print(f"   📍 Cities   : {', '.join(TARGET_CITIES)} (ya WFH)")
print(f"   ⭐ Priority : WFH first, office in target cities\n")

print("=" * 55)
print(f"✅ {len(candidates)} INTERNSHIPS MILI TUMHARE CRITERIA SE!")
print("=" * 55)

for rank, (sc, intern, matched) in enumerate(candidates, 1):
    mode_icon = "🏠 WFH" if intern["mode"] == "wfh" else "🏢 Office"
    print(f"\n#{rank}  {intern['title']}")
    print(f"     🏛️  Company  : {intern['company']}")
    print(f"     {mode_icon} | {intern['location']}")
    print(f"     💰 Stipend  : {intern['stipend']}")
    print(f"     🎯 Matched Skills: {', '.join(matched)}")
    print(f"     📊 Score    : {sc}")

# Jo reject hue - transparency ke liye dikhao
print("\n" + "=" * 55)
print(f"🚫 {len(rejected)} INTERNSHIPS FILTER OUT HUI")
print("=" * 55)
for intern, reason in rejected:
    print(f"   {reason} | {intern['title']} @ {intern['company']} ({intern['location']})")