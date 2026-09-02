# ============================================================
#   🎯 INTERNSHIP RADAR - CONFIG
#   Tumhari saari preferences YAHAN hain
# ============================================================

# Tumhari skills - 2 categories mein divide ki hain
MY_SKILLS = {
    # CORE skills - jinme tum STRONG ho (zyada weight milega)
    "core": ["Python", "Java", "sql", "Web scraping" , ""],

    # KNOWN skills - jo tumhe aati hain (kam weight)
    "known": ["HTML", "CSS", "JS", "Mysql", "Rest APIs", "FLask", "Redis", "Jinja", "Chart.js"],
}

# Target cities (office internships ke liye)
TARGET_CITIES = ["Delhi", "Ghaziabad", "Noida"]

# Mode preference: "wfh_first" = WFH ko zyada priority
MODE_PREFERENCE = "wfh_first"

# ---------- SCORING WEIGHTS (Points System) ----------
CORE_SKILL_WEIGHT = 15    # Har CORE skill match = 15 points
KNOWN_SKILL_WEIGHT = 8    # Har KNOWN skill match = 8 points
WFH_BONUS = 20            # WFH internship ka bonus
OFFICE_BONUS = 10         # Target city office ka bonus
MIN_SKILL_SCORE = 10      # Isse kam score = reject

# ---------- EMAIL ALERT SETTINGS ----------
SEND_EMAIL = True           # True karo toh email jayegi
SENDER_EMAIL = "snancy.01812@gmail.com"    
RECEIVER_EMAIL = "snancy.01812@gmail.com" 