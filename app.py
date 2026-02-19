import streamlit as st
import streamlit.components.v1 as components
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
ACCENT_A = "#7e80f1"   # indigo  — School A
ACCENT_B = "#f4556f"   # rose    — School B
ACCENT_P = "#addae5"   # amber   — Ranking parameters

# ─── GLOBAL STYLES ─────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

/* ── reset ── */
footer {{visibility:hidden;}}
#MainMenu {{visibility:hidden;}}
/* Keep header visible so sidebar toggle shows */
header[data-testid="stHeader"] {{
    background: {BG} !important;
    border-bottom: 1px solid {BORDER} !important;
}}
header[data-testid="stHeader"] button {{
    color: {TEXT} !important;
}}

/* ── app ── */
.stApp {{
    background: {BG};
    color: {TEXT};
    font-family: 'DM Sans', sans-serif;
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
    font-family: 'Space Mono', monospace !important;
}}
div[data-testid="stMetricDelta"] {{
    font-family: 'Space Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.72rem !important;
}}
div[data-testid="stMetricDelta"] svg {{
    width: 0.7rem !important;
    height: 0.7rem !important;
}}

/* ── section titles ── */
.sec-label {{
    font-family: 'Space Grotesk', sans-serif;
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
    font-family: 'Space Mono', monospace;
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

/* ── Dropdown borders: indigo for A (col 1), rose for B (col 2) ── */
/* Layout: A-stack(1) B-stack(2) buttons(3) county(4) */
[data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"]:first-of-type > [data-testid="stColumn"]:nth-child(1) [data-testid="stSelectbox"] > div > div {{
    border: 2px solid {ACCENT_A} !important;
    border-radius: 8px !important;
}}
[data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"]:first-of-type > [data-testid="stColumn"]:nth-child(2) [data-testid="stSelectbox"] > div > div {{
    border: 2px solid {ACCENT_B} !important;
    border-radius: 8px !important;
}}

/* ── Compare mode buttons — vertical alignment with dropdown stacks ── */
[data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"]:first-of-type > [data-testid="stColumn"]:nth-child(3) {{
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
}}
/* Neutral compare buttons — no accent color */
[data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"]:first-of-type > [data-testid="stColumn"]:nth-child(3) button {{
    background: transparent !important;
    border: 1px solid {BORDER} !important;
    color: {MUTED} !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
}}
[data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"]:first-of-type > [data-testid="stColumn"]:nth-child(3) button[kind="primary"] {{
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid {TEXT} !important;
    color: {TEXT} !important;
}}
.cmp-btn {{
    flex: 1;
    padding: 6px 10px;
    border-radius: 8px;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    text-align: center;
    cursor: pointer;
    border: 2px solid {BORDER};
    color: {MUTED};
    background: transparent;
    transition: all 0.15s ease;
}}
.cmp-btn.active {{
    background: rgba(196,232,12,0.10);
    border-color: {ACCENT_P};
    color: {ACCENT_P};
    box-shadow: 0 0 10px rgba(196,232,12,0.25);
}}
.cmp-btn:hover:not(.active) {{
    border-color: {MUTED};
    color: {TEXT};
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
/* select_slider: also target the value display span */
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] span,
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] div {{
    color: {ACCENT_P} !important;
}}

/* ── Slider track — neutralise fill via overlay ── */
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderTrack"] {{
    position: relative !important;
    overflow: hidden !important;
    background: {BORDER} !important;
}}
/* Overlay that covers the Streamlit fill completely */
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderTrack"]::after {{
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: {BORDER} !important;
    z-index: 1 !important;
    pointer-events: none !important;
    border-radius: inherit !important;
}}
/* Thumb must sit above the overlay */
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
    margin-bottom: -2px !important;
}}

/* ── Endpoint labels: CSS layer (JS MutationObserver handles hover) ── */
section[data-testid="stSidebar"] [data-testid="stTickBarMin"],
section[data-testid="stSidebar"] [data-testid="stTickBarMax"],
section[data-testid="stSidebar"] [data-testid="stTickBar"] {{
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
    overflow: hidden !important;
    position: absolute !important;
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
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    line-height: 1.2;
    flex: 1;
}}
.fit-card-badge {{
    font-family: 'Space Mono', monospace;
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
.fit-card-ring-inner {{
    width: 94px;
    height: 94px;
    border-radius: 50%;
    background: {CARD};
    display: flex;
    align-items: center;
    justify-content: center;
}}
.fit-card-score {{
    font-family: 'Space Mono', monospace;
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
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 900;
    line-height: 1;
    color: {TEXT};
}}
.fit-card-rank-of {{
    font-size: 0.62rem;
    font-weight: 600;
    color: {MUTED};
    font-family: 'Space Mono', monospace;
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
    font-family: 'DM Sans', sans-serif !important;
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
    font-family: 'DM Sans', sans-serif !important;
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
IMPORTANCE_LABELS = ["Ignore", "Low Importance", "Medium Importance", "High Importance", "Critical"]
IMPORTANCE_TO_NUM = {"Ignore": 0, "Low Importance": 2, "Medium Importance": 5, "High Importance": 8, "Critical": 10}

_NUM_TO_LABEL = {v: k for k, v in IMPORTANCE_TO_NUM.items()}
def _weight_to_label(w):
    closest = min(IMPORTANCE_TO_NUM.values(), key=lambda v: abs(v - w))
    return _NUM_TO_LABEL[closest]

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
    Calculate a Custom Fit Score (0-100) for every row.

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
            v_min, v_max = values.min(), values.max()
            if v_max == v_min:
                normalized = pd.Series(0.5, index=scored.index)
            else:
                normalized = (values - v_min) / (v_max - v_min)
            if metric.get("direction") == "lower":
                normalized = 1.0 - normalized
        else:  # target
            target = cfg.get("target", 50)
            max_distance = max(target, 100 - target, 1)  # avoid /0
            normalized = 1.0 - (values - target).abs() / max_distance
            normalized = normalized.clip(0, 1)

        weighted_sum += normalized * weight
        total_weight += weight

    if total_weight > 0:
        scored["Custom Fit Score"] = (weighted_sum / total_weight * 10).round(1)
    else:
        scored["Custom Fit Score"] = 5.0

    return scored.sort_values("Custom Fit Score", ascending=False)


# ─── SESSION DEFAULTS & SWAP ──────────────────────────────────────────
if "da_w" not in st.session_state:
    st.session_state["da_w"] = "Encinitas Union Elementary"
    st.session_state["sa_w"] = "El Camino Creek Elementary"
    st.session_state["db_w"] = "Del Mar Union Elementary"
    st.session_state["sb_w"] = "Sage Canyon"

def handle_swap():
    da, sa = st.session_state.da_w, st.session_state.sa_w
    db, sb = st.session_state.db_w, st.session_state.sb_w
    st.session_state.da_w, st.session_state.db_w = db, da
    st.session_state.sa_w, st.session_state.sb_w = sb, sa

# ─── TOP BAR — COUNTY + SCHOOL SELECTORS ──────────────────────────────
all_counties = sorted(df_master["County"].unique())

# ---------- district_mode via session state (replaces toggle) ----------
if "district_mode" not in st.session_state:
    st.session_state["district_mode"] = True

def _set_school_mode():
    st.session_state["district_mode"] = False
def _set_district_mode():
    st.session_state["district_mode"] = True

district_mode = st.session_state["district_mode"]

# ---------- layout: A-stack | B-stack | buttons | county --------
_col_a, _col_b, _col_btns, _col_county = st.columns(
    [1.2, 1.2, 1.0, 0.7], gap="small", vertical_alignment="bottom"
)

with _col_county:
    sel_county = st.selectbox("County", all_counties,
                              index=all_counties.index("San Diego") if "San Diego" in all_counties else 0,
                              label_visibility="collapsed")

county_df = df_master[df_master["County"] == sel_county]
districts = sorted(county_df["District"].unique())

with _col_a:
    da = st.selectbox("District A", districts, key="da_w", label_visibility="collapsed")
    sa_list = sorted(county_df[county_df["District"] == da]["School"].unique())
    sa = st.selectbox("School A", sa_list, key="sa_w", label_visibility="collapsed")

with _col_b:
    db = st.selectbox("District B", districts, key="db_w", label_visibility="collapsed")
    sb_list = sorted(county_df[county_df["District"] == db]["School"].unique())
    sb = st.selectbox("School B", sb_list, key="sb_w", label_visibility="collapsed")

with _col_btns:
    st.button("Compare Districts", on_click=_set_district_mode, use_container_width=True,
              type="primary" if district_mode else "secondary")
    st.button("Compare Schools", on_click=_set_school_mode, use_container_width=True,
              type="primary" if not district_mode else "secondary")

# ─── DYNAMIC GLOW on active dropdowns (school vs district mode) ──────
_first_block = '[data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"]:first-of-type'
if district_mode:
    # Glow on district dropdowns (1st widget in col 1 & 2), dim school (2nd)
    glow_css = f"""
    <style>
    {_first_block} > [data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) [data-testid="stSelectbox"] > div > div {{
        box-shadow: 0 0 8px 2px rgba(99,102,241,0.45) !important;
    }}
    {_first_block} > [data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) [data-testid="stSelectbox"] > div > div {{
        box-shadow: 0 0 8px 2px rgba(244,63,94,0.45) !important;
    }}
    {_first_block} > [data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) > div > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(2) [data-testid="stSelectbox"] > div > div,
    {_first_block} > [data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) > div > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(2) [data-testid="stSelectbox"] > div > div {{
        opacity: 0.4 !important;
        box-shadow: none !important;
    }}
    </style>
    """
else:
    # Glow on school dropdowns (2nd widget in col 1 & 2), dim district (1st)
    glow_css = f"""
    <style>
    {_first_block} > [data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) > div > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(2) [data-testid="stSelectbox"] > div > div {{
        box-shadow: 0 0 8px 2px rgba(99,102,241,0.45) !important;
    }}
    {_first_block} > [data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) > div > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(2) [data-testid="stSelectbox"] > div > div {{
        box-shadow: 0 0 8px 2px rgba(244,63,94,0.45) !important;
    }}
    {_first_block} > [data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) > div > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) [data-testid="stSelectbox"] > div > div,
    {_first_block} > [data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) > div > [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) [data-testid="stSelectbox"] > div > div {{
        opacity: 0.4 !important;
        box-shadow: none !important;
    }}
    </style>
    """
st.markdown(glow_css, unsafe_allow_html=True)

# ─── SIDEBAR — RANKING PARAMETERS ───────────────────────────────────
scoring_settings = {}

def _handle_reset():
    """Reset all weights to Medium Importance and targets to first directional option."""
    for _col, _cfg in METRIC_CONFIG.items():
        st.session_state[f"w_{_col}"] = "Medium Importance"
        if _cfg["type"] == "target":
            _opts = list(_cfg["options"].keys())
            st.session_state[f"t_{_col}"] = _opts[0]

with st.sidebar:
    # ── JS: MutationObserver — hide endpoint labels ──
    components.html("""
    <script>
    (function() {
        const TIDS = ['stTickBarMin', 'stTickBarMax', 'stTickBar'];
        function hide() {
            const doc = window.parent.document;
            const sidebar = doc.querySelector('[data-testid="stSidebar"]');
            if (!sidebar) return;
            TIDS.forEach(tid => {
                sidebar.querySelectorAll('[data-testid="' + tid + '"]').forEach(el => {
                    el.style.setProperty('display', 'none', 'important');
                });
            });
        }
        hide();
        const obs = new MutationObserver(hide);
        obs.observe(window.parent.document.body, {
            childList: true, subtree: true,
            attributes: true, attributeFilter: ['style', 'class']
        });
    })();
    </script>
    """, height=0)
    # ── reset button only (no title) ──
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    st.button("↺ Reset", on_click=_handle_reset, use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── IMPORTANCE SLIDERS (all metrics) ──
    for grp in CARD_GROUPS:
        for col in grp["keys"]:
            cfg = METRIC_CONFIG[col]

            # Seed session state with default if not already set
            if f"w_{col}" not in st.session_state:
                st.session_state[f"w_{col}"] = _weight_to_label(cfg["default_weight"])

            # For target metrics, show inline 2-choice text on same line as label
            if cfg["type"] == "target":
                opts = list(cfg["options"].keys())
                if len(opts) > 2:
                    opts = [opts[0], opts[-1]]
                if f"t_{col}" not in st.session_state:
                    st.session_state[f"t_{col}"] = opts[0]
                selected = st.session_state[f"t_{col}"]

                # Row: label left, two text-buttons right-justified
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
                imp_label = st.select_slider(
                    cfg["label"],
                    options=IMPORTANCE_LABELS,
                    key=f"w_{col}",
                    help=cfg.get("tip", ""),
                    label_visibility="collapsed",
                )
                w = IMPORTANCE_TO_NUM[imp_label]
                scoring_settings[col] = {"weight": w, "target": target_val}
            else:
                imp_label = st.select_slider(
                    cfg["label"],
                    options=IMPORTANCE_LABELS,
                    key=f"w_{col}",
                    help=cfg.get("tip", ""),
                )
                w = IMPORTANCE_TO_NUM[imp_label]
                scoring_settings[col] = {"weight": w}

# ─── RESOLVE DATA ─────────────────────────────────────────────────────
if not district_mode:
    data_a = county_df[county_df["School"] == sa].iloc[0]
    data_b = county_df[county_df["School"] == sb].iloc[0]
    label_a, label_b = sa, sb
    entity = "School"
else:
    data_a = county_df[county_df["District"] == da].mean(numeric_only=True)
    data_b = county_df[county_df["District"] == db].mean(numeric_only=True)
    label_a, label_b = da, db
    entity = "District"

# ─── CUSTOM FIT SCORE RANKINGS (top section) ───────────────────────────

# Score every school in the county
scored_county = calculate_custom_scores(county_df, scoring_settings)
scored_county["_rank"] = scored_county["Custom Fit Score"].rank(
    ascending=False, method="min").astype(int)
total_ranked = len(scored_county)

def _score_and_rank(label, col="School"):
    row = scored_county[scored_county[col] == label]
    if len(row):
        return row["Custom Fit Score"].values[0], int(row["_rank"].values[0])
    return None, None

if not district_mode:
    score_a, rank_a = _score_and_rank(label_a, "School")
    score_b, rank_b = _score_and_rank(label_b, "School")
else:
    # Build district-level aggregation for proper ranking
    _dist_scores = (scored_county.groupby("District")["Custom Fit Score"]
                    .mean().round(1).reset_index()
                    .sort_values("Custom Fit Score", ascending=False))
    _dist_scores["_rank"] = _dist_scores["Custom Fit Score"].rank(
        ascending=False, method="min").astype(int)
    total_ranked = len(_dist_scores)
    _row_a = _dist_scores[_dist_scores["District"] == label_a]
    _row_b = _dist_scores[_dist_scores["District"] == label_b]
    score_a = _row_a["Custom Fit Score"].values[0] if len(_row_a) else None
    rank_a  = int(_row_a["_rank"].values[0]) if len(_row_a) else None
    score_b = _row_b["Custom Fit Score"].values[0] if len(_row_b) else None
    rank_b  = int(_row_b["_rank"].values[0]) if len(_row_b) else None

def _fit_card(label, score, rank, school_color):
    s = f"{score:.1f}" if score is not None else "—"
    r_num = f"#{rank}" if rank is not None else "—"
    r_of = f"of {total_ranked}" if rank is not None else ""

    # Score-based gradient ring: green(≥9) → yellow(6) → red(≤3)
    if score is not None:
        clamped = min(max(score, 3.0), 9.0)
        pct = (clamped - 3.0) / 6.0  # 0—1 over the 3–9 range
        # Interpolate hue: 0 (red) at 3 → 60 (yellow) at 6 → 130 (green) at 9
        if pct <= 0.5:
            hue = int(pct * 2 * 60)        # 0→60
        else:
            hue = int(60 + (pct - 0.5) * 2 * 70)  # 60→130
        ring_color = f"hsl({hue}, 80%, 50%)"
        # Conic gradient: colored arc from 0 to score%, then dark for the rest
        arc_pct = min(max(score, 0), 10) / 10
        arc_deg = int(arc_pct * 360)
        ring_bg = f"conic-gradient({ring_color} 0deg, {ring_color} {arc_deg}deg, {BORDER} {arc_deg}deg, {BORDER} 360deg)"
    else:
        ring_bg = BORDER
        ring_color = MUTED

    # Compute rgba glow from school_color
    if school_color == ACCENT_A:
        glow_rgba = "99,102,241"
    else:
        glow_rgba = "244,63,94"

    return f"""
    <div class="fit-card" style="border-color:rgba({glow_rgba},0.3);box-shadow:0 4px 24px rgba({glow_rgba},0.15), inset 0 1px 0 rgba({glow_rgba},0.08);">
        <!-- Header: school name + entity badge -->
        <div class="fit-card-header">
            <div class="fit-card-name" style="color:{school_color};">{label}</div>
            <div class="fit-card-badge" style="background:rgba({glow_rgba},0.12);color:{school_color};">{entity}</div>
        </div>
        <!-- Body: score ring + rank box -->
        <div class="fit-card-body">
            <div class="fit-card-score-wrap">
                <div class="fit-card-ring" style="background:{ring_bg};">
                    <div class="fit-card-ring-inner">
                        <div class="fit-card-score" style="color:{ring_color};">{s}</div>
                    </div>
                </div>
                <div class="fit-card-score-label">Custom Fit Score</div>
            </div>
            <div class="fit-card-rank-wrap">
                <div class="fit-card-rank-num">{r_num}</div>
                <div class="fit-card-rank-of">{r_of}</div>
                <div class="fit-card-rank-label">County Rank</div>
            </div>
        </div>
    </div>
    """

cf_col_a, cf_col_b, cf_pad1, cf_pad2 = st.columns([1.2, 1.2, 1.0, 0.7], gap="small")
with cf_col_a:
    st.markdown(_fit_card(label_a, score_a, rank_a, ACCENT_A), unsafe_allow_html=True)
with cf_col_b:
    st.markdown(_fit_card(label_b, score_b, rank_b, ACCENT_B), unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:1.2rem;'></div>", unsafe_allow_html=True)

# Ranked table — aggregate to district level when in district mode
if district_mode:
    num_cols = ["Custom Fit Score", "SMATH_Y1", "SELA_Y1", "AVG_SIZE", "PERDI", "PEREL", "PERSD"]
    num_cols = [c for c in num_cols if c in scored_county.columns]
    scored_display = (
        scored_county.groupby("District")[num_cols]
        .mean()
        .round(1)
        .reset_index()
        .sort_values("Custom Fit Score", ascending=False)
    )
    scored_display["_rank"] = scored_display["Custom Fit Score"].rank(
        ascending=False, method="min").astype(int)
    total_ranked = len(scored_display)
    display_cols = ["District", "Custom Fit Score",
                    "SMATH_Y1", "SELA_Y1", "AVG_SIZE", "PERDI", "PEREL", "PERSD"]
    display_cols = [c for c in display_cols if c in scored_display.columns]
else:
    scored_display = scored_county
    display_cols = ["School", "District", "Custom Fit Score",
                    "SMATH_Y1", "SELA_Y1", "AVG_SIZE", "PERDI", "PEREL", "PERSD"]
    display_cols = [c for c in display_cols if c in scored_display.columns]

col_cfg = {
    "Custom Fit Score": st.column_config.NumberColumn(
        "Score",
        format="%.1f",
        width="6em",  # just enough for '10.0'
    ),
    "SMATH_Y1": st.column_config.NumberColumn("Math %",   format="%.1f", width="small"),
    "SELA_Y1":  st.column_config.NumberColumn("ELA %",    format="%.1f", width="small"),
    "AVG_SIZE": st.column_config.NumberColumn("Class Sz", format="%.1f", width="small"),
    "PERDI":    st.column_config.NumberColumn("Disadv %", format="%.1f", width="small"),
    "PEREL":    st.column_config.NumberColumn("EL %",     format="%.1f", width="small"),
    "PERSD":    st.column_config.NumberColumn("SWD %",    format="%.1f", width="small"),
}

# Build display dataframe and highlight School A / School B rows
_table_df = scored_display[display_cols].copy().reset_index(drop=True)
_match_col = "District" if district_mode else "School"

def _highlight_ab(row):
    """Return background style per row for school A (indigo) / school B (rose)."""
    val = row.get(_match_col, "")
    if val == label_a:
        return [f"background-color: rgba(99,102,241,0.18); color: {ACCENT_A}"] * len(row)
    elif val == label_b:
        return [f"background-color: rgba(244,63,94,0.18); color: {ACCENT_B}"] * len(row)
    return [""] * len(row)

def _score_bar(col):
    """CSS bar background per cell — color matches the card-ring hue."""
    styles = []
    for v in col:
        try:
            s = float(v)
        except (TypeError, ValueError):
            styles.append("")
            continue
        clamped = min(max(s, 3.0), 9.0)
        pct = (clamped - 3.0) / 6.0  # 0—1 over the 3–9 range
        if pct <= 0.5:
            hue = int(pct * 2 * 60)           # 0 → 60
        else:
            hue = int(60 + (pct - 0.5) * 2 * 70)  # 60 → 130
        c = f"hsl({hue}, 80%, 50%)"
        styles.append(
            f"background-color: {c}; color: #181818; font-weight: 700; text-align: center;"
        )
    return styles


# Set Custom Fit Score column width via Styler CSS

def _set_score_col_width(styler):
    # Set width for both cell and header using CSS with !important
    styler.set_table_styles([
        {"selector": "th.col_heading.level0.col0", "props": [
            ("min-width", "3.5em !important"),
            ("max-width", "3.5em !important"),
            ("width", "3.5em !important"),
            ("text-align", "center !important")
        ]},
        {"selector": "td.col0", "props": [
            ("min-width", "3.5em !important"),
            ("max-width", "3.5em !important"),
            ("width", "3.5em !important"),
            ("text-align", "center !important")
        ]},
    ], overwrite=False)
    return styler

_styled = (_table_df.style
           .apply(_highlight_ab, axis=1)
           .apply(_score_bar, subset=["Custom Fit Score"])
           .pipe(_set_score_col_width)
)

st.dataframe(
    _styled,
    column_config=col_cfg,
    use_container_width=True,
    hide_index=True,
    height=740,
)

with st.expander("Detailed Visual Comparisons", expanded=False):

    # ─── ROW 1 — CLASS SIZE GAUGE + PICTOGRAPH ────────────────────────────
    size_a_val = int(round(data_a["AVG_SIZE"]))
    size_b_val = int(round(data_b["AVG_SIZE"]))

    MAX_SEATS = 40  # total desk slots in the classroom grid

    def _icon(color, w_head, h_head, w_body, h_body, op="1"):
        """CSS person icon at arbitrary size."""
        return (
            f'<span style="display:inline-block;text-align:center;opacity:{op};">'
            f'<span style="display:block;width:{w_head}px;height:{h_head}px;border-radius:50%;'
            f'background:{color};margin:0 auto;"></span>'
            f'<span style="display:block;width:{w_body}px;height:{h_body}px;'
            f'border-radius:{w_body//2}px {w_body//2}px 2px 2px;'
            f'background:{color};margin:1px auto 0;"></span>'
            f'</span>'
        )

    def build_classroom(count, color, value):
        """Classroom card: top bar (number) · classroom grid below."""
        empty = "#252836"

        # ── TOP BAR: number left ──
        top_bar = (
            f'<div style="display:flex;align-items:center;'
            f'margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid {BORDER};">'
            f'<div style="display:flex;align-items:baseline;gap:6px;">'
            f'<span style="font-family:\'Space Mono\',monospace;font-size:1.6rem;'
            f'font-weight:700;color:{color};line-height:1;">{value:.1f}</span>'
            f'<span style="font-size:0.65rem;color:{MUTED};'
            f'font-family:Inter,sans-serif;">students</span>'
            f'</div>'
            f'</div>'
        )

        # ── CLASSROOM: teacher + wide student grid ──
        teacher_row = (
            f'<div style="text-align:center;margin-bottom:6px;">'
            f'{_icon(color, 8, 8, 12, 14)}'
            f'<div style="width:80%;max-width:120px;height:1px;background:{BORDER};'
            f'margin:4px auto 0;"></div>'
            f'</div>'
        )

        # 10 columns — uses full card width, only 4 rows
        cols = 10
        grid = ""
        for i in range(MAX_SEATS):
            if i % cols == 0:
                if i: grid += "</div>"
                grid += '<div style="display:flex;justify-content:center;gap:2px;margin:2px 0;">'
            fill = color if i < count else empty
            op = "1" if i < count else "0.22"
            grid += f'<span style="flex:0 0 auto;">{_icon(fill, 5, 5, 7, 9, op)}</span>'
        grid += "</div>"

        footer = (
            f'<div style="text-align:center;margin-top:6px;font-size:0.62rem;color:{MUTED};'
            f'font-family:Inter,sans-serif;letter-spacing:0.06em;">'
            f'{count} of {MAX_SEATS} seats</div>'
        )

        return (
            f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:8px;'
            f'padding:12px 16px 10px;">'
            f'{top_bar}{teacher_row}{grid}{footer}'
            f'</div>'
        )

    st.markdown('<div class="sec-label">Average Class Size</div>', unsafe_allow_html=True)
    c_class_a, c_class_b = st.columns([1, 1], gap="small")

    with c_class_a:
        st.markdown(build_classroom(size_a_val, ACCENT_A, data_a["AVG_SIZE"]), unsafe_allow_html=True)

    with c_class_b:
        st.markdown(build_classroom(size_b_val, ACCENT_B, data_b["AVG_SIZE"]), unsafe_allow_html=True)


    # ─── ROW 2 — PROFICIENCY BARS ──────────────────────────────────────────
    st.markdown('<div class="sec-label">Performance Profile</div>', unsafe_allow_html=True)

    # ── grouped bar — math & ela side-by-side ──
    subjects = ["Math Proficiency", "English Language Arts"]
    vals_a = [data_a["SMATH_Y1"], data_a["SELA_Y1"]]
    vals_b = [data_b["SMATH_Y1"], data_b["SELA_Y1"]]

    fig_b = go.Figure()
    fig_b.add_trace(go.Bar(
        x=subjects, y=vals_a, name=label_a,
        marker=dict(color=ACCENT_A, cornerradius=4),
        text=[f"{v:.1f}%" for v in vals_a], textposition="outside",
        textfont=dict(color=ACCENT_A, size=12, family="Space Mono", weight=700),
        width=0.32,
    ))
    fig_b.add_trace(go.Bar(
        x=subjects, y=vals_b, name=label_b,
        marker=dict(color=ACCENT_B, cornerradius=4),
        text=[f"{v:.1f}%" for v in vals_b], textposition="outside",
        textfont=dict(color=ACCENT_B, size=12, family="Space Mono", weight=700),
        width=0.32,
    ))
    fig_b.update_layout(
        **_PLT,
        height=300,
        barmode="group",
        yaxis=dict(range=[0, max(max(vals_a), max(vals_b)) * 1.25],
                   gridcolor=BORDER, gridwidth=1, tickfont=dict(color=MUTED, size=10),
                   showgrid=True),
        xaxis=dict(tickfont=dict(color=TEXT, size=11, family="Inter", weight=600)),
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    font=dict(size=10, color=MUTED)),
        showlegend=True,
        bargap=0.25,
    )
    st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})

    # ─── ROW 3 — DEMOGRAPHICS  ────────────────────────────────────────────
    st.markdown('<div class="sec-label">Demographics &amp; Enrollment</div>', unsafe_allow_html=True)
    c_eth, c_prog = st.columns([1, 1], gap="small")

    # ── butterfly chart — ethnicity ──
    with c_eth:
        eth_map = {
            "PERHI":    "Hispanic / Latino",
            "PERWH":    "White",
            "PERAS":    "Asian",
            "PERAA":    "Black",
            "PERMULTI": "Two+",
            "PERFI":    "Filipino",
        }
        rows = [{"L": n, "A": data_a.get(k, 0), "B": data_b.get(k, 0)} for k, n in eth_map.items()]
        eth = pd.DataFrame(rows).sort_values("A", ascending=True)

        fig_e = go.Figure()
        fig_e.add_trace(go.Bar(
            y=eth["L"], x=[-v for v in eth["A"]], orientation="h",
            marker=dict(color=ACCENT_A, cornerradius=3),
            text=[f"{v:.1f}%" for v in eth["A"]], textposition="inside",
            textfont=dict(color="white", size=10, family="Space Mono"),
            hovertemplate="%{y}: %{x:abs:.1f}%<extra>A</extra>",
            name=label_a,
        ))
        fig_e.add_trace(go.Bar(
            y=eth["L"], x=eth["B"].tolist(), orientation="h",
            marker=dict(color=ACCENT_B, cornerradius=3),
            text=[f"{v:.1f}%" for v in eth["B"]], textposition="inside",
            textfont=dict(color="white", size=10, family="Space Mono"),
            hovertemplate="%{y}: %{x:.1f}%<extra>B</extra>",
            name=label_b,
        ))
        fig_e.update_layout(
            **_PLT,
            height=300,
            barmode="relative",
            xaxis=dict(tickvals=[-80, -40, 0, 40, 80],
                       ticktext=["80%", "40%", "0", "40%", "80%"],
                       gridcolor=BORDER, zeroline=True, zerolinecolor=BORDER, zerolinewidth=1,
                       tickfont=dict(color=MUTED, size=9)),
            yaxis=dict(tickfont=dict(color=TEXT, size=10, family="Inter", weight=500)),
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                        font=dict(size=10, color=MUTED)),
            showlegend=True,
            bargap=0.2,
        )
        st.plotly_chart(fig_e, use_container_width=True, config={"displayModeBar": False})

    # ── horizontal grouped bar — program enrollment ──
    with c_prog:
        prog_map = {
            "PEREL": "English Learners",
            "PERDI": "Socio-Econ Disadv.",
            "PERSD": "Disabilities",
        }
        prog_rows = [{"L": n, "A": data_a.get(k, 0), "B": data_b.get(k, 0)} for k, n in prog_map.items()]
        # Fixed order: English Learners, Socio-Econ Disadv., Disabilities (reversed for horizontal bar)
        prog = pd.DataFrame(prog_rows)
        prog = prog.iloc[::-1].reset_index(drop=True)  # reverse so bottom-up reads top-down

        fig_p = go.Figure()
        fig_p.add_trace(go.Bar(
            y=prog["L"], x=prog["A"].tolist(), orientation="h",
            marker=dict(color=ACCENT_A, cornerradius=3),
            text=[f"{v:.1f}%" for v in prog["A"]], textposition="outside",
            textfont=dict(color=ACCENT_A, size=11, family="Space Mono", weight=600),
            name=label_a, width=0.35,
        ))
        fig_p.add_trace(go.Bar(
            y=prog["L"], x=prog["B"].tolist(), orientation="h",
            marker=dict(color=ACCENT_B, cornerradius=3),
            text=[f"{v:.1f}%" for v in prog["B"]], textposition="outside",
            textfont=dict(color=ACCENT_B, size=11, family="Space Mono", weight=600),
            name=label_b, width=0.35,
        ))
        fig_p.update_layout(
            **_PLT,
            height=300,
            barmode="group",
            xaxis=dict(gridcolor=BORDER, gridwidth=1,
                       tickfont=dict(color=MUTED, size=9),
                       range=[0, max(max(prog["A"]), max(prog["B"])) * 1.35]),
            yaxis=dict(tickfont=dict(color=TEXT, size=10, family="Inter", weight=500)),
            legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center",
                        font=dict(size=10, color=MUTED)),
            showlegend=True,
            bargap=0.25,
        )
        st.plotly_chart(fig_p, use_container_width=True, config={"displayModeBar": False})

# ─── FOOTER ────────────────────────────────────────────────────────────
st.markdown(
    '<div class="dash-footer">CAASPP Analytics · Custom Fit Score · All data from CA Dept. of Education</div>',
    unsafe_allow_html=True,
)

