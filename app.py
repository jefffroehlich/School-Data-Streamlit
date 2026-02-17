import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ─── CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CAASPP Performance Analytics",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── PALETTE ───────────────────────────────────────────────────────────
BG       = "#0c0e14"
SURFACE  = "#13151d"
CARD     = "#191c27"
BORDER   = "#252836"
TEXT     = "#e2e4ec"
MUTED    = "#6b7194"
ACCENT_A = "#6366f1"   # indigo
ACCENT_B = "#f43f5e"   # rose

# ─── GLOBAL STYLES ─────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

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
    width: 280px !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    padding: 1.2rem 1rem 1rem !important;
}}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown p {{
    color: {MUTED} !important;
    font-size: 0.65rem !important;
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
    font-size: 0.78rem !important;
}}

/* sidebar toggle */
section[data-testid="stSidebar"] .stToggle label {{
    font-size: 0.72rem !important;
    color: {TEXT} !important;
    letter-spacing: 0.04em !important;
}}

/* sidebar button */
section[data-testid="stSidebar"] .stButton button {{
    background: {CARD} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 6px !important;
    font-size: 0.68rem !important;
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
    font-size: 0.62rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}}
div[data-testid="stMetricValue"] > div {{
    color: {TEXT} !important;
    font-size: 1.55rem !important;
    font-weight: 800 !important;
    font-family: 'JetBrains Mono', monospace !important;
}}
div[data-testid="stMetricDelta"] {{
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.72rem !important;
}}
div[data-testid="stMetricDelta"] svg {{
    width: 0.7rem !important;
    height: 0.7rem !important;
}}

/* ── section titles ── */
.sec-label {{
    font-size: 0.62rem;
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
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    font-family: 'JetBrains Mono', monospace;
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
    font-size: 0.68rem;
    color: {MUTED};
    font-weight: 500;
    white-space: nowrap;
}}

/* ── sidebar custom labels ── */
.sb-group {{
    margin: 0.5rem 0 0.3rem;
    font-size: 0.6rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 5px 0;
    border-bottom: 2px solid;
}}
.sb-group-a {{ color: {ACCENT_A}; border-color: {ACCENT_A}; }}
.sb-group-b {{ color: {ACCENT_B}; border-color: {ACCENT_B}; }}

/* ── footer ── */
.dash-footer {{
    text-align: center;
    color: {MUTED};
    font-size: 0.6rem;
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

# ─── SESSION DEFAULTS & SWAP ──────────────────────────────────────────
if "da_w" not in st.session_state:
    st.session_state["da_w"] = "Encinitas Union Elementary"
    st.session_state["sa_w"] = "El Camino Creek Elementary"
    st.session_state["db_w"] = "Oceanside Unified"
    st.session_state["sb_w"] = "Oceanside High"

def handle_swap():
    da, sa = st.session_state.da_w, st.session_state.sa_w
    db, sb = st.session_state.db_w, st.session_state.sb_w
    st.session_state.da_w, st.session_state.db_w = db, da
    st.session_state.sa_w, st.session_state.sb_w = sb, sa

# ─── SIDEBAR ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
        <div style="margin-bottom:0.6rem;">
            <span style="font-size:0.9rem;font-weight:800;color:{TEXT};letter-spacing:-0.01em;">CAASPP</span>
            <span style="font-size:0.9rem;font-weight:300;color:{MUTED};margin-left:4px;">Analytics</span>
        </div>
    """, unsafe_allow_html=True)

    district_mode = st.toggle("School  ·  District", value=False)

    st.markdown("---")

    all_counties = sorted(df_master["County"].unique())
    sel_county = st.selectbox("COUNTY", all_counties,
                              index=all_counties.index("San Diego") if "San Diego" in all_counties else 0)
    county_df = df_master[df_master["County"] == sel_county]
    districts = sorted(county_df["District"].unique())

    st.markdown("---")

    # ── selection A ──
    st.markdown('<div class="sb-group sb-group-a">Selection A</div>', unsafe_allow_html=True)
    da = st.selectbox("DISTRICT", districts, key="da_w")
    sa_list = sorted(county_df[county_df["District"] == da]["School"].unique())
    sa = st.selectbox("SCHOOL", sa_list, key="sa_w")

    # ── selection B ──
    st.markdown('<div class="sb-group sb-group-b">Selection B</div>', unsafe_allow_html=True)
    db = st.selectbox("DISTRICT ", districts, key="db_w")
    sb_list = sorted(county_df[county_df["District"] == db]["School"].unique())
    sb = st.selectbox("SCHOOL ", sb_list, key="sb_w")

    st.markdown("---")
    st.button("⇅  SWAP A ↔ B", on_click=handle_swap, use_container_width=True)

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

# ─── HEADER BAR (one line, compact) ───────────────────────────────────
st.markdown(f"""
    <div class="dash-header">
        <span class="tag tag-a" style="font-size:0.82rem;padding:0.35rem 0.9rem;">{label_a}</span>
        <span style="color:{MUTED};font-size:0.7rem;font-weight:600;">vs</span>
        <span class="tag tag-b" style="font-size:0.82rem;padding:0.35rem 0.9rem;">{label_b}</span>
        <span style="flex:1;"></span>
        <span class="dash-sub">{entity} · {sel_county} County</span>
        <span class="dash-title" style="font-size:0.85rem;">◆&nbsp; Performance</span>
    </div>
""", unsafe_allow_html=True)

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
    """Classroom card: top bar (number + badge) · classroom grid below."""
    empty = "#252836"

    # ── badge ──
    if value <= 18:
        b_lbl, b_fg, b_bg = "COMFORTABLE", "#22c55e", "rgba(34,197,94,0.15)"
    elif value <= 24:
        b_lbl, b_fg, b_bg = "MODERATE", "#eab308", "rgba(234,179,8,0.15)"
    else:
        b_lbl, b_fg, b_bg = "CROWDED", "#ef4444", "rgba(239,68,68,0.15)"

    # ── TOP BAR: number left, badge right ──
    top_bar = (
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid {BORDER};">'
        f'<div style="display:flex;align-items:baseline;gap:6px;">'
        f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:1.6rem;'
        f'font-weight:700;color:{color};line-height:1;">{value:.1f}</span>'
        f'<span style="font-size:0.5rem;color:{MUTED};'
        f'font-family:Inter,sans-serif;">students</span>'
        f'</div>'
        f'<span style="background:{b_bg};color:{b_fg};'
        f'padding:3px 10px;border-radius:4px;font-size:0.55rem;font-weight:800;'
        f'letter-spacing:0.06em;font-family:\'JetBrains Mono\',monospace;">'
        f'{b_lbl}</span>'
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
        f'<div style="text-align:center;margin-top:6px;font-size:0.48rem;color:{MUTED};'
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
c_class_a, c_class_b, c_class_empty = st.columns([1, 1, 1.2], gap="small")

with c_class_a:
    st.markdown(build_classroom(size_a_val, ACCENT_A, data_a["AVG_SIZE"]), unsafe_allow_html=True)

with c_class_b:
    st.markdown(build_classroom(size_b_val, ACCENT_B, data_b["AVG_SIZE"]), unsafe_allow_html=True)

with c_class_empty:
    pass  # available for future content


# ─── ROW 2 — RADAR + PROFICIENCY BARS ─────────────────────────────────
st.markdown('<div class="sec-label">Performance Profile</div>', unsafe_allow_html=True)
c_radar, c_bars = st.columns([1, 1.3])

# ── radar ──
with c_radar:
    size_a = max(0, (40 - data_a["AVG_SIZE"]) * 2.5) if data_a["AVG_SIZE"] > 0 else 0
    size_b = max(0, (40 - data_b["AVG_SIZE"]) * 2.5) if data_b["AVG_SIZE"] > 0 else 0

    cats = ["Math", "ELA", "Class Size", "Math"]  # repeat first to close
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatterpolar(
        r=[data_a["SMATH_Y1"], data_a["SELA_Y1"], size_a, data_a["SMATH_Y1"]],
        theta=cats, fill="toself", name=label_a,
        line=dict(color=ACCENT_A, width=2),
        fillcolor="rgba(99,102,241,0.12)",
        marker=dict(size=6),
    ))
    fig_r.add_trace(go.Scatterpolar(
        r=[data_b["SMATH_Y1"], data_b["SELA_Y1"], size_b, data_b["SMATH_Y1"]],
        theta=cats, fill="toself", name=label_b,
        line=dict(color=ACCENT_B, width=2),
        fillcolor="rgba(244,63,94,0.12)",
        marker=dict(size=6),
    ))
    fig_r.update_layout(
        **{**_PLT, "margin": dict(t=25, b=25, l=50, r=50)},
        height=300,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False,
                            gridcolor=BORDER, gridwidth=1),
            angularaxis=dict(tickfont=dict(size=10, color=MUTED, family="Inter"),
                            gridcolor=BORDER, gridwidth=1.5),
        ),
        legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center",
                    font=dict(size=10, color=MUTED)),
        showlegend=True,
    )
    # Add reference triangle at 100% to show true bounds
    fig_r.add_trace(go.Scatterpolar(
        r=[100, 100, 100, 100],
        theta=cats,
        mode="lines",
        line=dict(color=BORDER, width=1, dash="dot"),
        showlegend=False,
        hoverinfo="skip",
    ))
    st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})

# ── grouped bar — math & ela side-by-side ──
with c_bars:
    subjects = ["Math Proficiency", "ELA Proficiency"]
    vals_a = [data_a["SMATH_Y1"], data_a["SELA_Y1"]]
    vals_b = [data_b["SMATH_Y1"], data_b["SELA_Y1"]]

    fig_b = go.Figure()
    fig_b.add_trace(go.Bar(
        x=subjects, y=vals_a, name=label_a,
        marker=dict(color=ACCENT_A, cornerradius=4),
        text=[f"{v:.1f}%" for v in vals_a], textposition="outside",
        textfont=dict(color=ACCENT_A, size=12, family="JetBrains Mono", weight=700),
        width=0.32,
    ))
    fig_b.add_trace(go.Bar(
        x=subjects, y=vals_b, name=label_b,
        marker=dict(color=ACCENT_B, cornerradius=4),
        text=[f"{v:.1f}%" for v in vals_b], textposition="outside",
        textfont=dict(color=ACCENT_B, size=12, family="JetBrains Mono", weight=700),
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
c_eth, c_prog = st.columns([1.3, 1])

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
        textfont=dict(color="white", size=10, family="JetBrains Mono"),
        hovertemplate="%{y}: %{x:abs:.1f}%<extra>A</extra>",
        name=label_a,
    ))
    fig_e.add_trace(go.Bar(
        y=eth["L"], x=eth["B"].tolist(), orientation="h",
        marker=dict(color=ACCENT_B, cornerradius=3),
        text=[f"{v:.1f}%" for v in eth["B"]], textposition="inside",
        textfont=dict(color="white", size=10, family="JetBrains Mono"),
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
        textfont=dict(color=ACCENT_A, size=11, family="JetBrains Mono", weight=600),
        name=label_a, width=0.35,
    ))
    fig_p.add_trace(go.Bar(
        y=prog["L"], x=prog["B"].tolist(), orientation="h",
        marker=dict(color=ACCENT_B, cornerradius=3),
        text=[f"{v:.1f}%" for v in prog["B"]], textposition="outside",
        textfont=dict(color=ACCENT_B, size=11, family="JetBrains Mono", weight=600),
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


