"""
School-Data Dash App  –  full port from Streamlit.

Run:  python dash_app.py
Then open http://127.0.0.1:8050
"""

import os
import pandas as pd
from dash import (Dash, html, dcc, dash_table, callback,
                  Input, Output, State, ALL, ctx, no_update)

# ─── PALETTE ───────────────────────────────────────────────────────────
BG       = "#0c0e14"
SURFACE  = "#13151d"
CARD     = "#191c27"
BORDER   = "#252836"
TEXT     = "#eaecf0"
MUTED    = "#bebfc5"
ACCENT_P = "#00d4ff"

# ─── DATA ──────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists("sarc_master.parquet"):
        return pd.read_parquet("sarc_master.parquet")
    return pd.DataFrame()

DF_MASTER = load_data()

# ─── METRIC CONFIGURATION ─────────────────────────────────────────────
CARD_GROUPS = [
    {"title": "Academic Excellence",  "keys": ["SMATH_Y1", "SELA_Y1"]},
    {"title": "Environment & Scale",  "keys": ["AVG_SIZE"]},
    {"title": "Student Demographics", "keys": ["PERDI", "PEREL", "PERSD"]},
]

# Flat ordered list of all metric columns (used everywhere)
ALL_METRIC_COLS = []
for _g in CARD_GROUPS:
    ALL_METRIC_COLS.extend(_g["keys"])

METRIC_CONFIG = {
    "SMATH_Y1": {
        "label": "Math Proficiency", "type": "linear", "direction": "higher",
        "default_weight": 8,
    },
    "SELA_Y1": {
        "label": "English Language Arts", "type": "linear", "direction": "higher",
        "default_weight": 8,
    },
    "AVG_SIZE": {
        "label": "Class Size", "type": "linear", "direction": "lower",
        "default_weight": 5,
    },
    "PERDI": {
        "label": "Socio-Econ Disadvantaged", "type": "target",
        "options": {"Affluent": 0, "Mixed": 50, "Disadvantaged": 100},
        "default_weight": 3,
    },
    "PEREL": {
        "label": "English Learners", "type": "target",
        "options": {"Few EL": 0, "Balanced": 50, "EL-Rich": 100},
        "default_weight": 3,
    },
    "PERSD": {
        "label": "Students w/ Disabilities", "type": "target",
        "options": {"Few SWD": 0, "Balanced": 50, "Inclusive": 100},
        "default_weight": 2,
    },
}

TARGET_COLS = [c for c in ALL_METRIC_COLS if METRIC_CONFIG[c]["type"] == "target"]

ALL_COUNTIES = sorted(DF_MASTER["County"].unique()) if len(DF_MASTER) else []
DEFAULT_COUNTY = "San Diego" if "San Diego" in ALL_COUNTIES else (ALL_COUNTIES[0] if ALL_COUNTIES else "")


# ─── SCORING ───────────────────────────────────────────────────────────
def calculate_custom_scores(df, settings):
    scored = df.copy()
    weighted_sum = pd.Series(0.0, index=scored.index)
    total_weight = 0
    for col, cfg in settings.items():
        weight = cfg.get("weight", 0)
        if weight == 0 or col not in scored.columns:
            continue
        values = pd.to_numeric(scored[col], errors="coerce")
        med = values.median()
        values = values.fillna(med if pd.notna(med) else 0)
        mc = METRIC_CONFIG.get(col, {})
        if mc.get("type") == "linear":
            norm = values.rank(pct=True)
            if mc.get("direction") == "lower":
                norm = 1.0 - norm
        else:
            target = cfg.get("target", 50)
            norm = 1.0 - (values - target).abs().rank(pct=True)
        norm = norm.clip(0, 1) ** 0.7
        weighted_sum += norm * weight
        total_weight += weight
    scored["Custom Fit Score"] = ((weighted_sum / total_weight * 10).round(1)
                                  if total_weight > 0 else 5.0)
    return scored.sort_values("Custom Fit Score", ascending=False)


def build_settings(weights, tgt_values):
    """Turn slider values + target prefs into the settings dict."""
    settings = {}
    tgt_i = 0
    for i, col in enumerate(ALL_METRIC_COLS):
        mc = METRIC_CONFIG[col]
        entry = {"weight": weights[i] if i < len(weights) else mc["default_weight"]}
        if mc["type"] == "target":
            pref = (tgt_values[tgt_i] if tgt_i < len(tgt_values)
                    else list(mc["options"].keys())[0])
            entry["target"] = mc["options"].get(pref, 50)
            tgt_i += 1
        settings[col] = entry
    return settings


def score_hue(score):
    if score is None:
        return 0
    clamped = min(max(score, 3.0), 9.0)
    pct = (clamped - 3.0) / 6.0
    return int(pct * 2 * 60) if pct <= 0.5 else int(60 + (pct - 0.5) * 2 * 70)


def score_bg(score):
    return f"hsl({score_hue(score)}, 80%, 50%)"


def build_lookups(scored, district_mode):
    """Return (lookup_dict, total_ranked, display_df)."""
    if district_mode:
        num_cols = [c for c in ["Custom Fit Score"] + ALL_METRIC_COLS if c in scored.columns]
        agg = (scored.groupby("District")[num_cols]
               .mean().round(1).reset_index()
               .sort_values("Custom Fit Score", ascending=False))
        agg["_rank"] = agg["Custom Fit Score"].rank(ascending=False, method="min").astype(int)
        lookup = dict(zip(agg["District"], zip(agg["Custom Fit Score"], agg["_rank"])))
        return lookup, len(agg), agg
    else:
        scored = scored.copy()
        scored["_rank"] = scored["Custom Fit Score"].rank(ascending=False, method="min").astype(int)
        lookup = {}
        for _, r in scored.iterrows():
            lookup[(r["District"], r["School"])] = (r["Custom Fit Score"], r["_rank"])
        return lookup, len(scored), scored


# ─── SIDEBAR BUILDER ──────────────────────────────────────────────────
def build_sidebar():
    children = [html.Button("↺ Reset", id="reset-btn", className="reset-btn",
                            style={"marginBottom": "12px"})]
    for grp in CARD_GROUPS:
        for col in grp["keys"]:
            mc = METRIC_CONFIG[col]
            row = []

            # --- label row ------------------------------------------------
            label_parts = [
                html.Span(mc["label"], className="sidebar-label", style={"flex": "1"}),
            ]
            if mc["type"] == "target":
                opts = list(mc["options"].keys())
                if len(opts) > 2:
                    opts = [opts[0], opts[-1]]
                label_parts.insert(1, html.Div([
                    html.Button(opts[0], id={"type": "tgt-btn", "col": col, "val": opts[0]},
                                className="tgt-btn active", n_clicks=0),
                    html.Button(opts[1], id={"type": "tgt-btn", "col": col, "val": opts[1]},
                                className="tgt-btn", n_clicks=0),
                ], className="tgt-btn-group"))
                row.append(dcc.Store(id={"type": "tgt-store", "col": col}, data=opts[0]))

            row.insert(0, html.Div(label_parts, className="sidebar-label-row"))

            # --- slider: NO tooltip, NO marks --------------------------
            row.append(dcc.Slider(
                id={"type": "weight-slider", "col": col},
                min=0, max=10, step=1, value=mc["default_weight"],
                marks=None, tooltip=None,
                className="sidebar-slider",
            ))
            children.append(html.Div(row, className="sidebar-metric-row"))
    return html.Div(children, id="sidebar")


# ─── APP ───────────────────────────────────────────────────────────────
app = Dash(__name__, suppress_callback_exceptions=True,
           title="School-Data Analytics", update_title=None)

app.layout = html.Div([
    dcc.Store(id="district-mode", data=True),
    dcc.Store(id="selections", data=[
        {"district": "Encinitas Union Elementary", "school": "El Camino Creek Elementary"},
        {"district": "Del Mar Union Elementary",   "school": "Sage Canyon"},
    ]),
    html.Div([
        build_sidebar(),
        html.Div([
            # Top bar
            html.Div([
                html.Button("Districts", id="mode-district", className="mode-btn active", n_clicks=0),
                html.Button("Schools",   id="mode-school",   className="mode-btn inactive", n_clicks=0),
                html.Div(dcc.Dropdown(
                    id="county-dropdown",
                    options=[{"label": c, "value": c} for c in ALL_COUNTIES],
                    value=DEFAULT_COUNTY, clearable=False, searchable=True,
                ), style={"minWidth": "200px", "marginLeft": "auto"}),
            ], id="top-bar"),
            # Selection cards — rendered entirely via callback
            html.Div(id="selection-cards"),
            html.Button("＋ Add", id="add-btn", className="add-btn", n_clicks=0),
            html.Div(style={"height": "1rem"}),
            # Data table
            dash_table.DataTable(
                id="data-table",
                style_header={
                    "backgroundColor": SURFACE, "color": MUTED, "fontWeight": "700",
                    "fontSize": "0.72rem", "textTransform": "uppercase",
                    "letterSpacing": "0.06em", "borderBottom": f"1px solid {BORDER}",
                    "padding": "8px 12px",
                },
                style_cell={
                    "backgroundColor": BG, "color": TEXT,
                    "fontFamily": "'Inter', sans-serif", "fontSize": "0.85rem",
                    "fontWeight": "500", "borderBottom": "1px solid rgba(37,40,54,0.5)",
                    "padding": "6px 12px", "textAlign": "left",
                    "whiteSpace": "nowrap", "overflow": "hidden", "textOverflow": "ellipsis",
                },
                style_data_conditional=[],
                page_size=50, sort_action="native", sort_mode="single",
                style_as_list_view=True,
            ),
            html.Div("CAASPP Analytics · Custom Fit Score · All data from CA Dept. of Education",
                      className="dash-footer"),
        ], id="main-content"),
    ], id="app-container"),
], id="root")


# ═══════════════════════════════════════════════════════════════════════
#  CALLBACKS
# ═══════════════════════════════════════════════════════════════════════

# ── Mode toggle ────────────────────────────────────────────────────────
@callback(
    Output("district-mode", "data"),
    Output("mode-district", "className"),
    Output("mode-school",   "className"),
    Input("mode-district", "n_clicks"),
    Input("mode-school",   "n_clicks"),
    prevent_initial_call=True,
)
def toggle_mode(n_dist, n_sch):
    if ctx.triggered_id == "mode-district":
        return True,  "mode-btn active", "mode-btn inactive"
    return False, "mode-btn inactive", "mode-btn active"


# ── Add / Remove selection ─────────────────────────────────────────────
@callback(
    Output("selections", "data"),
    Input("add-btn", "n_clicks"),
    Input({"type": "sel-remove", "index": ALL}, "n_clicks"),
    State("selections", "data"),
    State("county-dropdown", "value"),
    prevent_initial_call=True,
)
def manage_selections(add_clicks, remove_clicks, selections, county):
    triggered = ctx.triggered_id
    if triggered == "add-btn":
        cdf = DF_MASTER[DF_MASTER["County"] == county]
        dists = sorted(cdf["District"].unique())
        fd = dists[0] if dists else ""
        schs = sorted(cdf[cdf["District"] == fd]["School"].unique()) if fd else []
        selections.append({"district": fd, "school": schs[0] if schs else ""})
        return selections
    if isinstance(triggered, dict) and triggered.get("type") == "sel-remove":
        idx = triggered["index"]
        if len(selections) > 1 and 0 <= idx < len(selections):
            selections.pop(idx)
        return selections
    return no_update


# ── Render selection cards (scores computed inline — no second callback) ──
@callback(
    Output("selection-cards", "children"),
    Input("selections", "data"),
    Input("district-mode", "data"),
    Input("county-dropdown", "value"),
    Input({"type": "weight-slider", "col": ALL}, "value"),
    Input({"type": "tgt-store", "col": ALL}, "data"),
)
def render_cards(selections, district_mode, county, weights, tgt_values):
    county_df = DF_MASTER[DF_MASTER["County"] == county]
    districts = sorted(county_df["District"].unique())
    settings = build_settings(weights, tgt_values)
    scored = calculate_custom_scores(county_df, settings)
    lookup, total, _ = build_lookups(scored, district_mode)

    rows = []
    for i, sel in enumerate(selections):
        d = sel.get("district", districts[0] if districts else "")
        if d not in districts:
            d = districts[0] if districts else ""
        schs = sorted(county_df[county_df["District"] == d]["School"].unique())
        s = sel.get("school", schs[0] if schs else "")
        if s not in schs:
            s = schs[0] if schs else ""

        # lookup score
        sr = lookup.get(d) if district_mode else lookup.get((d, s))
        if sr:
            sc, rk = sr[0], int(sr[1])
            bg = score_bg(sc)
            score_children = [
                html.Div([html.Span(f"{sc:.1f}")],
                         className="score-circle", style={"background": bg}),
                html.Div([
                    html.Span(f"#{rk}", className="rank-num"),
                    html.Span(f"of {total} in {county} County", className="rank-ctx"),
                ], className="rank-text"),
            ]
        else:
            score_children = [
                html.Div([html.Span("—")], className="score-circle",
                         style={"background": BORDER}),
            ]

        rows.append(html.Div([
            html.Div(dcc.Dropdown(
                id={"type": "sel-district", "index": i},
                options=[{"label": x, "value": x} for x in districts],
                value=d, clearable=False, searchable=True,
            ), className="sel-dropdown-district"),
            html.Div(dcc.Dropdown(
                id={"type": "sel-school", "index": i},
                options=[{"label": x, "value": x} for x in schs],
                value=s, clearable=False, searchable=True,
                disabled=district_mode,
            ), className="sel-dropdown-school" + (" disabled" if district_mode else "")),
            html.Div(score_children, className="sel-score-area"),
            html.Button("✕", id={"type": "sel-remove", "index": i},
                        className="sel-remove-btn", n_clicks=0),
        ], className="sel-row", style={"marginBottom": "8px"}))

    return rows


# ── Sync district dropdown → store ────────────────────────────────────
@callback(
    Output("selections", "data", allow_duplicate=True),
    Input({"type": "sel-district", "index": ALL}, "value"),
    State("selections", "data"),
    State("county-dropdown", "value"),
    prevent_initial_call=True,
)
def sync_district(dist_values, selections, county):
    cdf = DF_MASTER[DF_MASTER["County"] == county]
    changed = False
    for i, dv in enumerate(dist_values):
        if i < len(selections) and dv and dv != selections[i].get("district"):
            selections[i]["district"] = dv
            schs = sorted(cdf[cdf["District"] == dv]["School"].unique())
            selections[i]["school"] = schs[0] if schs else ""
            changed = True
    return selections if changed else no_update


# ── Sync school dropdown → store ──────────────────────────────────────
@callback(
    Output("selections", "data", allow_duplicate=True),
    Input({"type": "sel-school", "index": ALL}, "value"),
    State("selections", "data"),
    prevent_initial_call=True,
)
def sync_school(sch_values, selections):
    changed = False
    for i, sv in enumerate(sch_values):
        if i < len(selections) and sv and sv != selections[i].get("school"):
            selections[i]["school"] = sv
            changed = True
    return selections if changed else no_update


# ── Data table ─────────────────────────────────────────────────────────
@callback(
    Output("data-table", "columns"),
    Output("data-table", "data"),
    Output("data-table", "style_data_conditional"),
    Input("selections", "data"),
    Input("district-mode", "data"),
    Input("county-dropdown", "value"),
    Input({"type": "weight-slider", "col": ALL}, "value"),
    Input({"type": "tgt-store", "col": ALL}, "data"),
)
def update_table(selections, district_mode, county, weights, tgt_values):
    county_df = DF_MASTER[DF_MASTER["County"] == county]
    settings = build_settings(weights, tgt_values)
    scored = calculate_custom_scores(county_df, settings)
    _, _, display_df = build_lookups(scored, district_mode)

    col_labels = {
        "Custom Fit Score": "⭐", "SMATH_Y1": "Math %", "SELA_Y1": "ELA %",
        "AVG_SIZE": "Class Sz", "PERDI": "Disadv %", "PEREL": "EL %", "PERSD": "SWD %",
    }
    data_cols = ["SMATH_Y1", "SELA_Y1", "AVG_SIZE", "PERDI", "PEREL", "PERSD"]
    if district_mode:
        show = ["Custom Fit Score", "District"] + [c for c in data_cols if c in display_df.columns]
    else:
        show = ["Custom Fit Score", "School", "District"] + [c for c in data_cols if c in display_df.columns]

    columns = [{"name": col_labels.get(c, c), "id": c,
                "type": "numeric" if c not in ("School", "District") else "text"}
               for c in show]
    records = display_df[show].to_dict("records")

    # Row highlighting
    cond = []
    for sel in selections:
        d, s = sel.get("district", ""), sel.get("school", "")
        if district_mode:
            fq = '{District} eq "' + d + '"'
        else:
            fq = '{District} eq "' + d + '" && {School} eq "' + s + '"'
        cond.append({"if": {"filter_query": fq},
                     "backgroundColor": "rgba(0,212,255,0.12)", "color": ACCENT_P})

    # Score column hue — use row_index for reliable matching
    for i, rec in enumerate(records):
        sv = rec.get("Custom Fit Score")
        if sv is not None:
            cond.append({
                "if": {"row_index": i, "column_id": "Custom Fit Score"},
                "backgroundColor": score_bg(sv),
                "color": "#181818", "fontWeight": "700", "textAlign": "center",
            })

    return columns, records, cond


# ── Target pref toggle ─────────────────────────────────────────────────
@callback(
    Output({"type": "tgt-store", "col": ALL}, "data"),
    Input({"type": "tgt-btn", "col": ALL, "val": ALL}, "n_clicks"),
    State({"type": "tgt-store", "col": ALL}, "data"),
    prevent_initial_call=True,
)
def toggle_target(_, current):
    triggered = ctx.triggered_id
    if not isinstance(triggered, dict):
        return no_update
    col, val = triggered["col"], triggered["val"]
    out = list(current)
    for i, tc in enumerate(TARGET_COLS):
        if tc == col:
            out[i] = val
    return out


# ── Reset ──────────────────────────────────────────────────────────────
@callback(
    Output({"type": "weight-slider", "col": ALL}, "value"),
    Output({"type": "tgt-store", "col": ALL}, "data", allow_duplicate=True),
    Input("reset-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reset_all(_):
    return ([METRIC_CONFIG[c]["default_weight"] for c in ALL_METRIC_COLS],
            [list(METRIC_CONFIG[c]["options"].keys())[0] for c in TARGET_COLS])


# ═══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app.run(debug=True, port=8050)
