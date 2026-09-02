# ============================================================
#   🎯 INTERNSHIP RADAR - CONFIG
#   Tumhari saari preferences YAHAN hain
# ============================================================

# Tumhari skills - 2 categories mein divide ki hain
MY_SKILLS = {
    # CORE skills - jinme tum STRONG ho (zyada weight milega)
    "core": ["python", "java", "sql", "web scraping"],

    # KNOWN skills - jo tumhe aati hain (kam weight)
    "known": ["html", "css", "js", "mysql", "rest api"],
}

# Target cities (office internships ke liye)
TARGET_CITIES = ["delhi", "ghaziabad", "noida"]

# Mode preference: "wfh_first" = WFH ko zyada priority
MODE_PREFERENCE = "wfh_first"

# ---------- SCORING WEIGHTS (Points System) ----------
CORE_SKILL_WEIGHT = 15    # Har CORE skill match = 15 points
KNOWN_SKILL_WEIGHT = 8    # Har KNOWN skill match = 8 points
WFH_BONUS = 20            # WFH internship ka bonus
OFFICE_BONUS = 10         # Target city office ka bonus
MIN_SKILL_SCORE = 10      # Isse kam score = reject