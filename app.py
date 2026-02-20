import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ─── CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Add Financial Testing",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── PALETTE ───────────────────────────────────────────────────────────
BG       = "#0c0e14"
SURFACE  = "#13151d"
CARD     = "#191c27"
BORDER   = "#252836"
TEXT     = "#eaecf0"
MUTED    = "#bebfc5"
ACCENT_A = "#4d67cd"   # indigo  — School A
ACCENT_B = "#f4556f"   # rose    — School B
ACCENT_P = "#00d4ff"   # cyan    — Ranking parameters

# ─── GLOBAL STYLES ─────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ── reset ── */
footer {{visibility:hidden;}}
#MainMenu {{visibility:hidden;}}
header[data-testid="stHeader"] {{
    display: none !important;
}}

/* ── app ── */
.stApp {{
    background: {BG};
    color: {TEXT};
    font-family: 'Inter', sans-serif;
}}
.block-container {{
    padding: 4.5rem 1.6rem 2rem !important;
    max-width: 100% !important;
}}

/* ── sidebar ── */
section[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px solid {BORDER} !important;
    width: 480px !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    padding: 0.8rem 0.8rem 1rem !important;
}}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown p {{
    color: {MUTED} !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}}
section[data-testid="stSidebar"] .stMarkdown h3 {{
    display: none !important;
}}

/* sidebar selectbox */
section[data-testid="stSidebar"] div[data-baseweb="select"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 6px !important;
}}
section[data-testid="stSidebar"] div[data-baseweb="select"]:focus-within {{
    border-color: {ACCENT_A} !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.15) !important;
}}
section[data-testid="stSidebar"] div[data-baseweb="select"] * {{
    color: {TEXT} !important;
    font-size: 0.82rem !important;
}}

/* sidebar toggle */
section[data-testid="stSidebar"] .stToggle label {{
    font-size: 0.78rem !important;
    color: {TEXT} !important;
    letter-spacing: 0.04em !important;
}}

/* sidebar button */
section[data-testid="stSidebar"] .stButton button {{
    background: {CARD} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 6px !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    padding: 0.5rem 1rem !important;
    text-transform: uppercase !important;
    transition: border-color 0.15s !important;
    box-shadow: none !important;
}}
section[data-testid="stSidebar"] .stButton button:hover {{
    border-color: {ACCENT_A} !important;
}}

/* sidebar divider */
section[data-testid="stSidebar"] hr {{
    border-color: {BORDER} !important;
    margin: 0.8rem 0 !important;
}}

/* ── metric cards ── */
div[data-testid="stMetric"] {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 0.9rem 1rem;
}}
div[data-testid="stMetricLabel"] > div {{
    color: {MUTED} !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}}
div[data-testid="stMetricValue"] > div {{
    color: {TEXT} !important;
    font-size: 1.55rem !important;
    font-weight: 800 !important;
    font-family: 'Inter', sans-serif !important;
}}
div[data-testid="stMetricDelta"] {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.72rem !important;
}}
div[data-testid="stMetricDelta"] svg {{
    width: 0.7rem !important;
    height: 0.7rem !important;
}}

/* ── section titles ── */
.sec-label {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    color: {MUTED};
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin: 1.4rem 0 0.6rem;
    padding-bottom: 0.35rem;
    border-bottom: 1px solid {BORDER};
}}

/* ── tags / badges ── */
.tag {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    font-family: 'Inter', sans-serif;
}}
.tag-a {{ background: rgba(99,102,241,0.15); color: {ACCENT_A}; }}
.tag-b {{ background: rgba(244,63,94,0.15); color: {ACCENT_B}; }}

/* ── header bar ── */
.dash-header {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid {BORDER};
}}
.dash-title {{
    font-size: 1.05rem;
    font-weight: 800;
    color: {TEXT};
    letter-spacing: -0.01em;
    white-space: nowrap;
}}
.dash-sub {{
    font-size: 0.75rem;
    color: {MUTED};
    font-weight: 500;
    white-space: nowrap;
}}

/* ── sidebar custom labels ── */
.sb-group {{
    margin: 0.5rem 0 0.3rem;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 5px 0;
    border-bottom: 2px solid;
}}
.sb-group-a {{ color: {ACCENT_P}; border-color: {ACCENT_P}; }}
.sb-group-b {{ color: {ACCENT_P}; border-color: {ACCENT_P}; }}

/* ── footer ── */
.dash-footer {{
    text-align: center;
    color: {MUTED};
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    padding: 1rem 0 0.5rem;
    margin-top: 1.5rem;
    border-top: 1px solid {BORDER};
}}

/* ── hide default H1-H3 top padding ── */
h1, h2, h3 {{ margin-top: 0 !important; }}

/* ── scrollbar ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {BG}; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: {MUTED}; }}

/* ── plotly modebar hide ── */
.modebar {{ display: none !important; }}

/* ── Score circle column: strip stMarkdown margin so circle aligns with dropdown ── */
[data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] [data-testid="stMarkdownContainer"] {{
    display: flex !important;
    align-items: center !important;
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}}
[data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] [data-testid="element-container"] {{
    margin-bottom: 0 !important;
}}

/* ── Main content selectbox: large bold selected value ── */
[data-testid="stMainBlockContainer"] [data-testid="stSelectbox"] div[data-baseweb="select"] span {{
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    color: {TEXT} !important;
    letter-spacing: -0.01em !important;
}}
[data-testid="stMainBlockContainer"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div > div > div:first-child {{
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    color: {TEXT} !important;
    letter-spacing: -0.01em !important;
}}

/* ──────────────────────────────────────────────────────  */
/* RANKING SIDEBAR — Grid Layout                      */
/* ──────────────────────────────────────────────────────  */

/* ── Metric row: consistent height for alignment ── */
.metric-grid-row {{
    min-height: 62px;
    padding: 4px 0;
    border-bottom: 1px solid rgba(37,40,54,0.5);
}}
.metric-grid-row:last-child {{
    border-bottom: none;
}}

/* ── Slider thumb (dot) = accent color ── */
section[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {{
    background: {ACCENT_P} !important;
    border-color: {ACCENT_P} !important;
}}

/* ── Importance value text = accent color ── */
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] {{
    color: {ACCENT_P} !important;
    font-weight: 800 !important;
    font-size: 0.7rem !important;
    background: transparent !important;
}}
/* Slider: also target the value display span */
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] span,
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] div {{
    color: {ACCENT_P} !important;
}}

/* ── Slider track ── */
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderTrack"] {{
    background: {BORDER} !important;
}}
/* Filled portion of the track = ACCENT_P */
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderTrack"] > div:first-child {{
    background: {ACCENT_P} !important;
}}
/* Thumb must sit above the track */
section[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {{
    position: relative !important;
    z-index: 2 !important;
    background: {ACCENT_P} !important;
    border-color: {ACCENT_P} !important;
}}
/* Thumb value must sit above overlay too */
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] {{
    position: relative !important;
    z-index: 3 !important;
}}

/* ── Metric label above slider = neutral muted ── */
section[data-testid="stSidebar"] [data-testid="stSlider"] label p {{
    color: {MUTED} !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}}

/* ── Compact slider vertical spacing ── */
section[data-testid="stSidebar"] [data-testid="stSlider"] {{
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    margin-bottom: 8px !important;
}}

/* ── Slider min/max labels: hide for clean look ── */
section[data-testid="stSidebar"] [data-testid="stTickBarMin"],
section[data-testid="stSidebar"] [data-testid="stTickBarMax"],
section[data-testid="stSidebar"] [data-testid="stTickBar"] {{
    display: none !important;
}}

/* ── Target segmented control — accent highlight + vertical center ── */
.tgt-col {{
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 62px;
}}
.tgt-col [data-testid="stSegmentedControl"] {{
    margin-top: 8px;
}}
.tgt-col [data-testid="stSegmentedControl"] button {{
    font-size: 0.64rem !important;
    padding: 4px 8px !important;
    letter-spacing: 0.03em !important;
    flex: 1 1 0% !important;
    min-width: 0 !important;
}}
.tgt-col [data-testid="stSegmentedControl"] button[aria-checked="true"] {{
    background: rgba(107,53,183,0.18) !important;
    color: {ACCENT_P} !important;
    border-color: rgba(107,53,183,0.35) !important;
    font-weight: 700 !important;
}}

/* ── Reset button ── */
.reset-btn button {{
    background: transparent !important;
    border: 1px dashed {BORDER} !important;
    color: {MUTED} !important;
    font-size: 0.68rem !important;
    padding: 0.3rem 0.6rem !important;
    border-radius: 8px !important;
    letter-spacing: 0.06em !important;
}}
.reset-btn button:hover {{
    border-color: {ACCENT_P} !important;
    color: {ACCENT_P} !important;
}}

/* ── Add selection button ── */
.add-btn button {{
    background: transparent !important;
    border: 1px dashed {BORDER} !important;
    color: {MUTED} !important;
    font-size: 0.72rem !important;
    padding: 0.35rem 1rem !important;
    border-radius: 8px !important;
    letter-spacing: 0.06em !important;
}}
.add-btn button:hover {{
    border-color: {ACCENT_P} !important;
    color: {ACCENT_P} !important;
}}

/* ── Custom Fit Score Hero Cards ── */
.fit-card {{
    background: linear-gradient(135deg, {CARD} 0%, rgba(25,28,39,0.95) 100%);
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 0;
    overflow: hidden;
    position: relative;
}}
.fit-card-header {{
    padding: 14px 20px 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
}}
.fit-card-name {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    line-height: 1.2;
    flex: 1;
}}
.fit-card-badge {{
    font-family: 'Inter', sans-serif;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    padding: 4px 10px;
    border-radius: 20px;
    white-space: nowrap;
    text-transform: uppercase;
}}
.fit-card-body {{
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 20px 18px;
    gap: 24px;
}}
.fit-card-score-wrap {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}}
/* Gradient ring around score number */
.fit-card-ring {{
    width: 110px;
    height: 110px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}}
.fit-card-score {{
    font-family: 'Inter', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.03em;
}}
.fit-card-score-label {{
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {MUTED};
}}
.fit-card-rank-wrap {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    padding: 10px 16px;
    border-radius: 10px;
    background: rgba(0,0,0,0.25);
    min-width: 80px;
}}
.fit-card-rank-num {{
    font-family: 'Inter', sans-serif;
    font-size: 2rem;
    font-weight: 900;
    line-height: 1;
    color: {TEXT};
}}
.fit-card-rank-of {{
    font-size: 0.62rem;
    font-weight: 600;
    color: {MUTED};
    font-family: 'Inter', sans-serif;
}}
.fit-card-rank-label {{
    font-size: 0.55rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {MUTED};
    margin-top: 2px;
}}
.fit-card-bar {{
    height: 4px;
    width: 100%;
    border-radius: 0;
}}
.fit-card-bar-fill {{
    height: 100%;
    border-radius: 0 2px 2px 0;
    transition: width 0.4s ease;
}}



/* ── compact top bar selectors ── */
.top-bar-row {{
    display: flex;
    align-items: center;
    gap: 0.4rem;
    flex-wrap: wrap;
}}

/* ── target preference inline text-buttons ── */
section[data-testid="stSidebar"] .stMarkdown p.tgt-lbl {{
    color: {MUTED} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.4 !important;
}}
/* Make target buttons look like plain text — match category header font */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stBaseButton-secondary"],
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stBaseButton-primary"] {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 3px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: {MUTED} !important;
    opacity: 0.45;
    min-height: 0 !important;
    height: auto !important;
    line-height: 1.3 !important;
    white-space: nowrap !important;
    transition: opacity 0.15s, color 0.15s !important;
}}
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stBaseButton-secondary"]:hover {{
    opacity: 0.8;
    color: {TEXT} !important;
}}
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stBaseButton-primary"] {{
    color: {ACCENT_P} !important;
    opacity: 1;
    text-decoration: underline !important;
    text-underline-offset: 3px !important;
}}

</style>
""", unsafe_allow_html=True)

# ─── PLOTLY THEME DEFAULTS ─────────────────────────────────────────────
_PLT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color=MUTED, size=11),
    margin=dict(t=10, b=30, l=10, r=10),
    hoverlabel=dict(bgcolor=CARD, font_size=11, font_family="Inter", bordercolor=BORDER),
)

# ─── DATA ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    if os.path.exists("sarc_master.parquet"):
        return pd.read_parquet("sarc_master.parquet")
    return pd.DataFrame()

df_master = load_data()

# ─── METRIC CONFIGURATION ──────────────────────────────────────────────

# ─── Card groups ───
CARD_GROUPS = [
    {
        "title": "Academic Excellence",
        "icon":  "ðŸŽ“",
        "css":   "a",
        "keys":  ["SMATH_Y1", "SELA_Y1"],
    },
    {
        "title": "Environment & Scale",
        "icon":  "ðŸ«",
        "css":   "c",
        "keys":  ["AVG_SIZE"],
    },
    {
        "title": "Student Demographics",
        "icon":  "ðŸ‘¥",
        "css":   "b",
        "keys":  ["PERDI", "PEREL", "PERSD"],
    },
]

METRIC_CONFIG = {
    "SMATH_Y1": {
        "label": "Math Proficiency",
        "group": "Academic Performance",
        "type": "linear",
        "direction": "higher",
        "default_weight": 8,
        "tip": "Higher values favour schools with stronger math CAASPP scores.",
    },
    "SELA_Y1": {
        "label": "English Language Arts",
        "group": "Academic Performance",
        "type": "linear",
        "direction": "higher",
        "default_weight": 8,
        "tip": "Higher values favour schools with stronger ELA CAASPP scores.",
    },
    "AVG_SIZE": {
        "label": "Class Size",
        "group": "Environment",
        "type": "linear",
        "direction": "lower",
        "default_weight": 5,
        "tip": "Higher importance favours schools with smaller average class sizes.",
    },
    "PERDI": {
        "label": "Socio-Econ Disadvantaged",
        "group": "Student Demographics",
        "type": "target",
        "options": {"Affluent": 0, "Mixed": 50, "Disadvantaged": 100},
        "default_weight": 3,
        "default_pref": "Affluent",
        "tip": "Affluent targets <10 %, Mixed ≈50 %, Disadvantaged targets >90 %.",
    },
    "PEREL": {
        "label": "English Learners",
        "group": "Student Demographics",
        "type": "target",
        "options": {"Few EL": 0, "Balanced": 50, "EL-Rich": 100},
        "default_weight": 3,
        "default_pref": "Few EL",
        "tip": "Few EL targets <10 %, Balanced ≈50 %, EL-Rich targets >90 % English Learner students.",
    },
    "PERSD": {
        "label": "Students w/ Disabilities",
        "group": "Student Demographics",
        "type": "target",
        "options": {"Few SWD": 0, "Balanced": 50, "Inclusive": 100},
        "default_weight": 2,
        "default_pref": "Few SWD",
        "tip": "Few SWD targets <10 %, Balanced ≈50 %, Inclusive targets >90 % Students w/ Disabilities.",
    },
}


def calculate_custom_scores(df, settings):
    """
    Calculate a Custom Fit Score (0–10) for every row.

    Uses percentile-rank normalisation with a concave curve (x^0.7)
    so that above-average schools score closer to 10 while poor fits
    still separate clearly toward 0.

    Parameters
    ----------
    df : pd.DataFrame
        School-level data (must contain the columns referenced in *settings*).
    settings : dict
        {column: {"weight": int, "target": float (target metrics only)}}.

    Returns
    -------
    pd.DataFrame  –  copy of *df* with a 'Custom Fit Score' column, sorted desc.
    """
    scored = df.copy()
    weighted_sum = pd.Series(0.0, index=scored.index)
    total_weight = 0

    for col, cfg in settings.items():
        weight = cfg.get("weight", 0)
        if weight == 0 or col not in scored.columns:
            continue

        values = pd.to_numeric(scored[col], errors="coerce")
        median_val = values.median()
        values = values.fillna(median_val if pd.notna(median_val) else 0)

        metric = METRIC_CONFIG.get(col, {})
        metric_type = metric.get("type", "linear")

        if metric_type == "linear":
            # Percentile rank (0-1): immune to outlier skew
            normalized = values.rank(pct=True)
            if metric.get("direction") == "lower":
                normalized = 1.0 - normalized
        else:  # target
            target = cfg.get("target", 50)
            distance = (values - target).abs()
            # Smaller distance = better fit → higher percentile
            normalized = 1.0 - distance.rank(pct=True)

        # Concave curve: pushes above-average scores toward 1.0
        normalized = normalized.clip(0, 1) ** 0.7

        weighted_sum += normalized * weight
        total_weight += weight

    if total_weight > 0:
        scored["Custom Fit Score"] = (weighted_sum / total_weight * 10).round(1)
    else:
        scored["Custom Fit Score"] = 5.0

    return scored.sort_values("Custom Fit Score", ascending=False)



# ─── SESSION STATE ─────────────────────────────────────────────────────
if "sel_ids" not in st.session_state:
    st.session_state["sel_ids"] = [0, 1]
    st.session_state["sel_next_id"] = 2
    st.session_state["dist_0"] = "Encinitas Union Elementary"
    st.session_state["sch_0"]  = "El Camino Creek Elementary"
    st.session_state["dist_1"] = "Del Mar Union Elementary"
    st.session_state["sch_1"]  = "Sage Canyon"

if "district_mode" not in st.session_state:
    st.session_state["district_mode"] = True


def _set_school_mode():
    st.session_state["district_mode"] = False


def _set_district_mode():
    st.session_state["district_mode"] = True


def _add_selection():
    nid = st.session_state["sel_next_id"]
    st.session_state["sel_ids"].append(nid)
    st.session_state["sel_next_id"] = nid + 1


def _remove_selection(sid):
    if len(st.session_state["sel_ids"]) > 1:
        st.session_state["sel_ids"].remove(sid)


district_mode = st.session_state["district_mode"]
all_counties = sorted(df_master["County"].unique())

# ─── TOP BAR — MODE BUTTONS + COUNTY ──────────────────────────────────
_col_mode, _col_spacer, _col_county = st.columns(
    [1.2, 3.0, 0.8], gap="small", vertical_alignment="bottom"
)

with _col_mode:
    _m1, _m2 = st.columns(2)
    with _m1:
        st.button("Districts", on_click=_set_district_mode, use_container_width=True,
                  type="primary" if district_mode else "secondary", key="mode_dist")
    with _m2:
        st.button("Schools", on_click=_set_school_mode, use_container_width=True,
                  type="primary" if not district_mode else "secondary", key="mode_sch")

with _col_county:
    sel_county = st.selectbox("County", all_counties,
                              index=all_counties.index("San Diego") if "San Diego" in all_counties else 0,
                              label_visibility="collapsed",
                              key="county_sel")

county_df = df_master[df_master["County"] == sel_county]
districts = sorted(county_df["District"].unique())

# ─── SIDEBAR — RANKING PARAMETERS ───────────────────────────────────
scoring_settings = {}


def _handle_reset():
    """Reset all weights to default and targets to first directional option."""
    for _col, _cfg in METRIC_CONFIG.items():
        st.session_state[f"w_{_col}"] = _cfg["default_weight"]
        if _cfg["type"] == "target":
            _opts = list(_cfg["options"].keys())
            st.session_state[f"t_{_col}"] = _opts[0]


with st.sidebar:
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    st.button("↺ Reset", on_click=_handle_reset, use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)

    for grp in CARD_GROUPS:
        for col in grp["keys"]:
            cfg = METRIC_CONFIG[col]

            if f"w_{col}" not in st.session_state:
                st.session_state[f"w_{col}"] = cfg["default_weight"]

            if cfg["type"] == "target":
                opts = list(cfg["options"].keys())
                if len(opts) > 2:
                    opts = [opts[0], opts[-1]]
                if f"t_{col}" not in st.session_state:
                    st.session_state[f"t_{col}"] = opts[0]
                selected = st.session_state[f"t_{col}"]

                _lbl_c, _b1_c, _b2_c = st.columns([5, 1.4, 1.4], vertical_alignment="center")
                with _lbl_c:
                    st.markdown(
                        f'<p class="tgt-lbl">{cfg["label"]}</p>',
                        unsafe_allow_html=True,
                    )
                with _b1_c:
                    st.button(
                        opts[0], key=f"targetbtn_{col}_0",
                        on_click=lambda c=col, v=opts[0]: st.session_state.update({f"t_{c}": v}),
                        use_container_width=True,
                        type="primary" if selected == opts[0] else "secondary",
                    )
                with _b2_c:
                    st.button(
                        opts[1], key=f"targetbtn_{col}_1",
                        on_click=lambda c=col, v=opts[1]: st.session_state.update({f"t_{c}": v}),
                        use_container_width=True,
                        type="primary" if selected == opts[1] else "secondary",
                    )

                target_val = cfg["options"].get(selected, 50)
                w = st.slider(
                    cfg["label"],
                    min_value=0, max_value=10, step=1,
                    key=f"w_{col}",
                    help=cfg.get("tip", ""),
                    label_visibility="collapsed",
                )
                scoring_settings[col] = {"weight": w, "target": target_val}
            else:
                w = st.slider(
                    cfg["label"],
                    min_value=0, max_value=10, step=1,
                    key=f"w_{col}",
                    help=cfg.get("tip", ""),
                )
                scoring_settings[col] = {"weight": w}

# ─── SCORING ──────────────────────────────────────────────────────────
scored_county = calculate_custom_scores(county_df, scoring_settings)
scored_county["_rank"] = scored_county["Custom Fit Score"].rank(
    ascending=False, method="min").astype(int)
total_ranked = len(scored_county)

# Build immutable lookup dicts so selection cards can't mutate scores
# Use (District, School) composite key — some school names exist in multiple districts
_school_scores = {}
for _, _r in scored_county.iterrows():
    _school_scores[(_r["District"], _r["School"])] = (_r["Custom Fit Score"], _r["_rank"])

if district_mode:
    _num_cols = ["Custom Fit Score", "SMATH_Y1", "SELA_Y1", "AVG_SIZE", "PERDI", "PEREL", "PERSD"]
    _num_cols = [c for c in _num_cols if c in scored_county.columns]
    _dist_agg = (
        scored_county.groupby("District")[_num_cols]
        .mean().round(1).reset_index()
        .sort_values("Custom Fit Score", ascending=False)
    )
    _dist_agg["_rank"] = _dist_agg["Custom Fit Score"].rank(
        ascending=False, method="min").astype(int)
    total_ranked = len(_dist_agg)
    _dist_scores = dict(zip(_dist_agg["District"],
                            zip(_dist_agg["Custom Fit Score"],
                                _dist_agg["_rank"])))


def _get_score_rank(name, district=None):
    """Get score and rank for a school or district from pre-built lookup."""
    if district_mode:
        sr = _dist_scores.get(name)
    else:
        sr = _school_scores.get((district, name))
    if sr:
        return sr[0], int(sr[1])
    return None, None


def _score_hue(score):
    """HSL hue: red(3) -> yellow(6) -> green(9)."""
    if score is None:
        return 0
    clamped = min(max(score, 3.0), 9.0)
    pct = (clamped - 3.0) / 6.0
    if pct <= 0.5:
        return int(pct * 2 * 60)
    return int(60 + (pct - 0.5) * 2 * 70)


def _mini_score_html(score, rank):
    """Compact score circle + rank text for selection cards."""
    if score is not None:
        hue = _score_hue(score)
        bg = f"hsl({hue}, 80%, 50%)"
        s_text = f"{score:.1f}"
    else:
        bg = BORDER
        s_text = "—"
    r_num = f"#{rank}" if rank else ""
    r_ctx = f"of {total_ranked} in {sel_county} County" if rank else ""
    return f"""
    <div style="display:flex;align-items:center;gap:14px;">
        <div style="width:48px;height:48px;border-radius:50%;background:{bg};
            display:flex;align-items:center;justify-content:center;flex-shrink:0;">
            <span style="font-family:'Inter',sans-serif;font-size:1.1rem;font-weight:900;
                color:{CARD};letter-spacing:-0.02em;">{s_text}</span>
        </div>
        <div style="display:flex;align-items:baseline;gap:6px;">
            <span style="font-family:'Inter',sans-serif;font-size:1.6rem;font-weight:900;
                color:{TEXT};letter-spacing:-0.03em;line-height:1;">{r_num}</span>
            <span style="font-family:'Inter',sans-serif;font-size:1.0rem;font-weight:500;
                color:{MUTED};white-space:nowrap;">{r_ctx}</span>
        </div>
    </div>
    """


# ─── SELECTION CARDS ──────────────────────────────────────────────────
selected_labels = []

for sid in st.session_state["sel_ids"]:
    # Always render both dropdowns so session state stays in sync across modes
    _c_dist, _c_sch, _c_score, _c_rm = st.columns(
        [1.2, 1.2, 3, 0.3], gap="small", vertical_alignment="center"
    )
    with _c_dist:
        d = st.selectbox("District", districts, key=f"dist_{sid}",
                         label_visibility="collapsed")
    sch_list = sorted(county_df[county_df["District"] == d]["School"].unique())
    with _c_sch:
        s = st.selectbox("School", sch_list, key=f"sch_{sid}",
                         label_visibility="collapsed",
                         disabled=district_mode)
    if district_mode:
        score, rank = _get_score_rank(d)
        selected_labels.append(d)
    else:
        score, rank = _get_score_rank(s, district=d)
        selected_labels.append((d, s))
    with _c_score:
        st.markdown(_mini_score_html(score, rank), unsafe_allow_html=True)
    with _c_rm:
        if len(st.session_state["sel_ids"]) > 1:
            st.button("✕", key=f"rm_{sid}",
                      on_click=_remove_selection, args=(sid,))

# Add button
st.markdown('<div class="add-btn">', unsafe_allow_html=True)
st.button("＋ Add", on_click=_add_selection, use_container_width=False)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:1.2rem;'></div>", unsafe_allow_html=True)

# ─── DATA TABLE ───────────────────────────────────────────────────────
if district_mode:
    scored_display = _dist_agg
    display_cols = ["Custom Fit Score", "District",
                    "SMATH_Y1", "SELA_Y1", "AVG_SIZE", "PERDI", "PEREL", "PERSD"]
else:
    scored_display = scored_county
    display_cols = ["Custom Fit Score", "School", "District",
                    "SMATH_Y1", "SELA_Y1", "AVG_SIZE", "PERDI", "PEREL", "PERSD"]

display_cols = [c for c in display_cols if c in scored_display.columns]

col_cfg = {
    "Custom Fit Score": st.column_config.NumberColumn("⭐", format="%.1f", width=25),
    "SMATH_Y1": st.column_config.NumberColumn("Math %",   format="%.1f", width="small"),
    "SELA_Y1":  st.column_config.NumberColumn("ELA %",    format="%.1f", width="small"),
    "AVG_SIZE": st.column_config.NumberColumn("Class Sz", format="%.1f", width="small"),
    "PERDI":    st.column_config.NumberColumn("Disadv %", format="%.1f", width="small"),
    "PEREL":    st.column_config.NumberColumn("EL %",     format="%.1f", width="small"),
    "PERSD":    st.column_config.NumberColumn("SWD %",    format="%.1f", width="small"),
}

_table_df = scored_display[display_cols].copy().reset_index(drop=True)
_selected_set = set(selected_labels)


def _highlight_selected(row):
    """Highlight rows matching any user selection."""
    if district_mode:
        val = row.get("District", "")
    else:
        val = (row.get("District", ""), row.get("School", ""))
    if val in _selected_set:
        return [f"background-color: rgba(0,212,255,0.12); color: {ACCENT_P}"] * len(row)
    return [""] * len(row)


def _score_bar(col):
    """CSS bar background per cell -- hue matches score."""
    styles = []
    for v in col:
        try:
            s = float(v)
        except (TypeError, ValueError):
            styles.append("")
            continue
        clamped = min(max(s, 3.0), 9.0)
        pct = (clamped - 3.0) / 6.0
        if pct <= 0.5:
            hue = int(pct * 2 * 60)
        else:
            hue = int(60 + (pct - 0.5) * 2 * 70)
        c = f"hsl({hue}, 80%, 50%)"
        styles.append(
            f"background-color: {c}; color: #181818; font-weight: 700; text-align: center;"
        )
    return styles


_styled = (_table_df.style
           .apply(_highlight_selected, axis=1)
           .apply(_score_bar, subset=["Custom Fit Score"])
)

st.dataframe(
    _styled,
    column_config=col_cfg,
    use_container_width=True,
    hide_index=True,
    height=740,
)

# ─── FOOTER ────────────────────────────────────────────────────────────
st.markdown(
    '<div class="dash-footer">CAASPP Analytics · Custom Fit Score · All data from CA Dept. of Education</div>',
    unsafe_allow_html=True,
)
