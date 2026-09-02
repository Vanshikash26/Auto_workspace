import streamlit as st
import pandas as pd
import fetcher
import config

# ============================================================
#   MATCHING LOGIC
# ============================================================
SKILL_ALIASES = {
    "js": "javascript", "gzb": "ghaziabad", "scraping": "web scraping",
    "rest": "rest api", "rest-api": "rest api", "restful": "rest api",
    "postgres": "sql", "postgresql": "sql",
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

def is_location_ok(job):
    if job["mode"].lower() == "wfh":
        return True
    city = normalize_city(job["location"])
    return any(t in city or city in t for t in TARGET_CITIES)

def calculate_total_score(job):
    skill_score, matched_core, matched_known = calculate_skill_score(job["skills"])
    if job["mode"].lower() == "wfh":
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
#   💙 BABY BLUE PRO THEME (No White, Professional Sidebar)
# ============================================================
st.set_page_config(page_title="InternShip Radar", page_icon="🎯", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700&display=swap');

    html, body { background: #E9F3FC !important; }
    .stApp { background: linear-gradient(180deg, #EAF4FD, #DDEBFA); }

    /* ---- SAARI HEADINGS: Same Navy (jaise 'Job Details') ---- */
    h1, h2, h3, h4 {
        font-family: 'Poppins', sans-serif !important;
        color: #14365C !important;
        font-weight: 700 !important;
        background: none !important;
        -webkit-text-fill-color: #14365C !important;
    }
    h1 { font-size: 2.5rem !important; letter-spacing: -0.5px; }

    .stMarkdown p { font-size: 1rem; color: #46688F; }

    /* ---- Button ---- */
    .stButton > button {
        background: linear-gradient(90deg, #1F6FEB, #1450A3) !important;
        color: #EAF4FD !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.85rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 2px 10px rgba(31,111,235,0.25) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 16px rgba(31,111,235,0.35) !important;
    }

    /* ---- Metric Cards (Baby Blue, no white) ---- */
    [data-testid="stMetric"] {
        background: #DDEBFA;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 8px rgba(20,54,92,0.08);
        border: 1px solid #B9D4EE;
        border-left: 4px solid #1F6FEB;
        transition: all 0.25s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 16px rgba(31,111,235,0.15);
    }
    [data-testid="stMetricLabel"] { color: #46688F; font-weight: 600; }
    [data-testid="stMetricValue"] { color: #14365C; font-family: 'Poppins'; font-weight: 700; }

    /* ---- PROFESSIONAL SIDEBAR ---- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #DCEBFA, #CFE2F7);
        border-right: 1px solid #B9D4EE;
    }
    [data-testid="stSidebar"] .stMarkdown p { color: #46688F; }

    /* ---- Table ---- */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 8px rgba(20,54,92,0.08);
        border: 1px solid #B9D4EE;
        background: #DDEBFA;
    }

    /* ---- Job Cards ---- */
    [data-testid="stExpander"] {
        background: #DDEBFA;
        border-radius: 12px;
        border: 1px solid #B9D4EE;
        box-shadow: 0 1px 6px rgba(20,54,92,0.06);
        margin-bottom: 10px;
    }
    [data-testid="stExpander"] summary { font-weight: 600; color: #14365C; }
    [data-testid="stExpander"] p { color: #46688F; }

    .stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
#   PROFESSIONAL SIDEBAR (Brand + Clean Sections + Skill Chips)
# ============================================================
def sidebar_label(text):
    st.sidebar.markdown(
        f'<div style="font-size:0.72rem;font-weight:700;letter-spacing:1.5px;'
        f'text-transform:uppercase;color:#1F6FEB;margin:16px 0 6px 0;">{text}</div>',
        unsafe_allow_html=True)

def skill_chips(skills):
    chips = "".join(
        f'<span style="display:inline-block;background:#CFE3F8;color:#14365C;'
        f'border:1px solid #B9D4EE;border-radius:20px;padding:4px 12px;'
        f'margin:3px 4px 3px 0;font-size:0.78rem;font-weight:600;">{s}</span>'
        for s in skills)
    st.sidebar.markdown(chips, unsafe_allow_html=True)

with st.sidebar:
    # Brand header
    st.sidebar.markdown("""
    <div style="padding:4px 0 14px 0;border-bottom:2px solid #B9D4EE;margin-bottom:10px;">
      <div style="font-family:'Poppins',sans-serif;font-size:1.2rem;font-weight:700;color:#14365C;">🎯 InternShip Radar</div>
      <div style="font-size:0.78rem;color:#46688F;margin-top:2px;">Smart Internship Discovery</div>
    </div>
    """, unsafe_allow_html=True)

    sidebar_label("Core Skills")
    skill_chips(config.MY_SKILLS["core"])

    sidebar_label("Known Skills")
    skill_chips(config.MY_SKILLS["known"])

    sidebar_label("Target Cities")
    skill_chips(config.TARGET_CITIES)

    st.sidebar.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    st.sidebar.info("Edit `config.py` to update your profile.")

# ============================================================
#   MAIN UI
# ============================================================
st.title("🎯 InternShip Radar")
st.markdown("Discover remote internships that match **your skills** — powered by live data.")

if st.button("🔍 Find Matching Jobs", type="primary", use_container_width=True):

    with st.spinner("Fetching live jobs from the internet..."):
        jobs = fetcher.fetch_remote_jobs(limit=100)

    if not jobs:
        st.error("Could not fetch jobs. Please check your internet and try again.")
    else:
        candidates = []
        for job in jobs:
            if not is_location_ok(job):
                continue
            details = calculate_total_score(job)
            if details["skill_score"] < config.MIN_SKILL_SCORE:
                continue
            candidates.append({**job, **details})

        candidates.sort(key=lambda x: x["total"], reverse=True)

        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Jobs Fetched", len(jobs))
        col2.metric("Matched", len(candidates))
        col3.metric("Top Score", candidates[0]["total"] if candidates else "—")

        if candidates:
            st.success(f"Found {len(candidates)} jobs matching your skills!")

            st.subheader("Matched Jobs")
            table_data = []
            for c in candidates[:20]:
                table_data.append({
                    "Title": c["title"],
                    "Company": c["company"],
                    "Mode": c["mode_label"],
                    "Location": c["location"],
                    "Score": c["total"],
                })
            st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

            st.subheader("Job Details")
            for c in candidates[:10]:
                with st.expander(f"{c['title']} @ {c['company']} — Score: {c['total']}"):
                    st.write(f"**Mode:** {c['mode_label']}")
                    st.write(f"**Location:** {c['location']}")
                    st.write(f"**Stipend:** {c['stipend']}")
                    st.write(f"**Posted:** {c['posted']}")
                    if c["matched_core"]:
                        st.write(f"**Core Skills Matched:** {', '.join(c['matched_core'])}")
                    if c["matched_known"]:
                        st.write(f"**Known Skills Matched:** {', '.join(c['matched_known'])}")
                    if c.get("url"):
                        st.write(f"**Apply:** {c['url']}")
        else:
            st.warning("No matching jobs found. Try updating your skills in `config.py`.")