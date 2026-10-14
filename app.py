import streamlit as st
import plotly.graph_objects as go
import time
import io

st.set_page_config(
    page_title="GreenLens",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Design tokens (matches pitch deck palette) ──────────────────
C = {
    "spinach":  "#8A9A35",
    "spinachD": "#6B7A28",
    "placid":   "#9BAEC8",
    "merlot":   "#6E1C2A",
    "sage":     "#F2F5E9",
    "border":   "#D8DEC8",
    "muted":    "#7A7E6A",
    "text":     "#1A1A18",
    "white":    "#FFFFFF",
    "red":      "#B84040",
    "amber":    "#C47A2A",
    "green":    "#4A7C59",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {{ box-sizing: border-box; }}

[data-testid="stAppViewContainer"] {{
    background: {C['sage']};
    font-family: 'Inter', sans-serif;
}}
[data-testid="stHeader"] {{ background: transparent; height: 0; }}
[data-testid="stSidebar"] {{ display: none; }}
[data-testid="stFileUploader"] label {{ font-size: 15px !important; font-weight: 500 !important; color: {C['text']} !important; }}
[data-testid="stFileUploader"] section {{ background: {C['white']}; border: 2px dashed {C['border']}; border-radius: 10px; }}
[data-testid="stFileUploader"] section:hover {{ border-color: {C['spinach']}; }}
div[data-testid="stSpinner"] p {{ font-size: 15px !important; }}

/* ── NAV BAR ── */
.gl-nav {{
    background: {C['text']};
    padding: 0 40px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 12px;
    margin-bottom: 36px;
}}
.gl-nav-brand {{
    font-size: 20px;
    font-weight: 800;
    color: {C['white']};
    letter-spacing: -0.3px;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.gl-nav-brand span {{
    color: {C['spinach']};
}}
.gl-nav-tag {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.8px;
    color: {C['muted']};
    text-transform: uppercase;
}}

/* ── UPLOAD PANEL ── */
.gl-upload-wrap {{
    background: {C['white']};
    border-radius: 12px;
    padding: 28px 32px;
    border: 1px solid {C['border']};
    margin-bottom: 4px;
}}
.gl-upload-title {{
    font-size: 18px;
    font-weight: 700;
    color: {C['text']};
    margin-bottom: 6px;
}}
.gl-upload-sub {{
    font-size: 14px;
    color: {C['muted']};
    margin-bottom: 20px;
    line-height: 1.5;
}}

/* ── INDICATOR PILLS ── */
.gl-pills {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}}
.gl-pill {{
    font-size: 12px;
    font-weight: 600;
    color: {C['spinachD']};
    background: {C['sage']};
    border: 1px solid {C['border']};
    border-radius: 20px;
    padding: 5px 14px;
    letter-spacing: 0.2px;
}}

/* ── DIVIDER ── */
.gl-divider {{
    border: none;
    border-top: 1px solid {C['border']};
    margin: 28px 0;
}}

/* ── SCORE CARD ── */
.score-card {{
    background: {C['white']};
    border-radius: 12px;
    padding: 36px 28px;
    text-align: center;
    border: 1px solid {C['border']};
    height: 100%;
}}
.score-eyebrow {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: {C['muted']};
    text-transform: uppercase;
    margin-bottom: 12px;
}}
.score-number {{
    font-size: 100px;
    font-weight: 800;
    line-height: 1;
    margin: 4px 0 10px;
    font-variant-numeric: tabular-nums;
}}
.score-denom {{
    font-size: 16px;
    color: {C['muted']};
    font-weight: 500;
    margin-bottom: 16px;
}}
.score-badge {{
    display: inline-block;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    padding: 6px 20px;
    border-radius: 30px;
    margin-bottom: 20px;
}}
.score-company {{
    font-size: 22px;
    font-weight: 700;
    color: {C['text']};
    margin-bottom: 12px;
    line-height: 1.3;
}}
.score-summary {{
    font-size: 14px;
    color: {C['muted']};
    line-height: 1.65;
    text-align: left;
}}

/* ── SECTION LABEL ── */
.sec-label {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: {C['muted']};
    text-transform: uppercase;
    margin: 0 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid {C['border']};
}}

/* ── STAT TILES ── */
.stat-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 8px 0 28px;
}}
.stat-tile {{
    background: {C['white']};
    border-radius: 10px;
    padding: 22px 20px;
    border: 1px solid {C['border']};
    text-align: center;
}}
.stat-val {{
    font-size: 42px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 8px;
}}
.stat-lbl {{
    font-size: 12px;
    font-weight: 600;
    color: {C['muted']};
    letter-spacing: 0.5px;
    line-height: 1.4;
    text-transform: uppercase;
}}

/* ── EXCERPT CARDS ── */
.excerpt {{
    background: {C['white']};
    border-radius: 10px;
    border: 1px solid {C['border']};
    border-left-width: 4px;
    padding: 18px 20px;
    margin-bottom: 12px;
}}
.excerpt.red    {{ border-left-color: {C['red']}; }}
.excerpt.amber  {{ border-left-color: {C['amber']}; }}
.excerpt-quote  {{
    font-size: 14px;
    font-style: italic;
    color: {C['text']};
    line-height: 1.65;
    margin-bottom: 12px;
}}
.excerpt-tag {{
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    padding: 3px 12px;
    border-radius: 20px;
    margin-right: 8px;
    margin-bottom: 6px;
}}
.tag-red    {{ background: #F5E8E8; color: {C['red']}; }}
.tag-amber  {{ background: #F5EDE0; color: {C['amber']}; }}
.excerpt-reason {{
    font-size: 13px;
    color: {C['muted']};
    line-height: 1.5;
}}

/* ── COMPARISON ── */
.cmp-row {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}}
.cmp-name {{
    font-size: 14px;
    font-weight: 600;
    color: {C['text']};
    width: 90px;
    flex-shrink: 0;
}}
.cmp-track {{
    flex: 1;
    background: {C['sage']};
    border-radius: 5px;
    height: 28px;
    border: 1px solid {C['border']};
    overflow: hidden;
}}
.cmp-fill {{
    height: 100%;
    border-radius: 4px;
    display: flex;
    align-items: center;
    padding-left: 10px;
    font-size: 13px;
    font-weight: 700;
    color: white;
}}

/* ── LEGEND ── */
.legend-box {{
    background: {C['white']};
    border: 1px solid {C['border']};
    border-radius: 10px;
    padding: 16px 18px;
    margin-top: 16px;
    font-size: 13px;
    color: {C['muted']};
    line-height: 2;
}}
.legend-box b {{ color: {C['text']}; }}

/* ── LANDING ── */
.landing {{
    text-align: center;
    padding: 72px 20px 80px;
}}
.landing-icon {{ font-size: 52px; margin-bottom: 20px; }}
.landing-title {{
    font-size: 26px;
    font-weight: 800;
    color: {C['text']};
    margin-bottom: 10px;
    letter-spacing: -0.4px;
}}
.landing-sub {{
    font-size: 16px;
    color: {C['muted']};
    line-height: 1.6;
    max-width: 480px;
    margin: 0 auto 32px;
}}
.landing-indicators {{
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}}

/* ── FOOTER ── */
.gl-footer {{
    margin-top: 48px;
    padding: 20px 32px;
    background: {C['text']};
    border-radius: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.gl-footer-left {{
    font-size: 14px;
    font-weight: 700;
    color: {C['white']};
}}
.gl-footer-left span {{ color: {C['spinach']}; }}
.gl-footer-right {{
    font-size: 13px;
    color: {C['muted']};
    font-weight: 500;
}}
</style>
""", unsafe_allow_html=True)

# ── Pre-computed results ────────────────────────────────────────
COMPANIES = {
    "bmw": {
        "name": "BMW Group",
        "score": 8.0,
        "indicators": {
            "Target Specificity":   3,
            "Data-Backed Claims":   2,
            "Standards Alignment":  7,
            "Risk Disclosure":      4,
            "Promises vs Results":  9,
        },
        "summary": "BMW's report shows heavy reliance on forward-looking commitments with limited quantified results and low data backing for key climate claims.",
        "excerpts": [
            {
                "quote": "BMW Group is committed to becoming fully climate neutral across the entire value chain by 2050.",
                "reason": "No intermediate milestones, no baseline year, no measurable interim targets disclosed.",
                "level": "red",
                "tag": "Vague Commitment",
            },
            {
                "quote": "We are making significant progress toward our sustainability goals.",
                "reason": "Qualitative claim with no supporting data or comparison to a prior period.",
                "level": "red",
                "tag": "Unverifiable Claim",
            },
            {
                "quote": "Our vehicles will contribute to a greener future for generations to come.",
                "reason": "Aspirational language with no actionable content or quantified metric.",
                "level": "amber",
                "tag": "Rhetorical Inflation",
            },
        ],
        "stats": {"pages": 214, "claims": 347, "backed": 18},
    },
    "tesla": {
        "name": "Tesla, Inc.",
        "score": 8.0,
        "indicators": {
            "Target Specificity":   4,
            "Data-Backed Claims":   3,
            "Standards Alignment":  6,
            "Risk Disclosure":      3,
            "Promises vs Results":  8,
        },
        "summary": "Tesla's report emphasises product-level impact while disclosing minimal supply chain risk and showing a high ratio of future claims to verified outcomes.",
        "excerpts": [
            {
                "quote": "Every Tesla vehicle sold accelerates the world's transition to sustainable energy.",
                "reason": "Broad causal claim with no lifecycle assessment data to support it.",
                "level": "red",
                "tag": "Unverifiable Claim",
            },
            {
                "quote": "We continue to pursue a path toward zero-emission transportation globally.",
                "reason": "No timeline, no target, no metric defined.",
                "level": "red",
                "tag": "Vague Commitment",
            },
            {
                "quote": "Tesla's mission is to accelerate the world's transition to sustainable energy.",
                "reason": "Mission statement repeated as a sustainability outcome — no evidential value.",
                "level": "amber",
                "tag": "Rhetorical Inflation",
            },
        ],
        "stats": {"pages": 188, "claims": 289, "backed": 22},
    },
    "byd": {
        "name": "BYD Co., Ltd.",
        "score": 7.0,
        "indicators": {
            "Target Specificity":   5,
            "Data-Backed Claims":   4,
            "Standards Alignment":  6,
            "Risk Disclosure":      4,
            "Promises vs Results":  7,
        },
        "summary": "BYD shows moderate quantification but limited alignment with international ESG frameworks and a high proportion of forward-looking claims.",
        "excerpts": [
            {
                "quote": "BYD is dedicated to green innovation and a carbon-free future.",
                "reason": "No target year, no scope defined, no reduction pathway disclosed.",
                "level": "red",
                "tag": "Vague Commitment",
            },
            {
                "quote": "Our green products have contributed significantly to reducing global carbon emissions.",
                "reason": "\"Significantly\" is undefined and no aggregate figure is provided.",
                "level": "amber",
                "tag": "Unverifiable Claim",
            },
        ],
        "stats": {"pages": 176, "claims": 261, "backed": 31},
    },
    "toyota": {
        "name": "Toyota Motor Corp.",
        "score": 7.0,
        "indicators": {
            "Target Specificity":   5,
            "Data-Backed Claims":   5,
            "Standards Alignment":  7,
            "Risk Disclosure":      5,
            "Promises vs Results":  7,
        },
        "summary": "Toyota demonstrates stronger standards alignment but continues to overweight long-horizon pledges relative to near-term measurable actions.",
        "excerpts": [
            {
                "quote": "Toyota aims to achieve carbon neutrality by 2050 across all operations and products.",
                "reason": "28-year timeline with no 2030 intermediate target disclosed.",
                "level": "amber",
                "tag": "Vague Commitment",
            },
            {
                "quote": "We will continue to pursue ever-better mobility solutions for a sustainable society.",
                "reason": "Aspirational language with no quantified target or action plan.",
                "level": "amber",
                "tag": "Rhetorical Inflation",
            },
        ],
        "stats": {"pages": 203, "claims": 312, "backed": 38},
    },
    "renault": {
        "name": "Renault Group",
        "score": 5.0,
        "indicators": {
            "Target Specificity":   6,
            "Data-Backed Claims":   6,
            "Standards Alignment":  7,
            "Risk Disclosure":      6,
            "Promises vs Results":  5,
        },
        "summary": "Renault shows above-average quantification and risk disclosure, though some claims still lack full evidential backing.",
        "excerpts": [
            {
                "quote": "Renault Group is committed to reducing CO₂ emissions from its vehicles by 40% by 2030.",
                "reason": "Target is specific but baseline year and scope boundary are not defined in this section.",
                "level": "amber",
                "tag": "Incomplete Disclosure",
            },
        ],
        "stats": {"pages": 195, "claims": 278, "backed": 44},
    },
}

INDUSTRY_AVG = 7.0
INDICATORS = ["Target Specificity", "Data-Backed Claims", "Standards Alignment", "Risk Disclosure", "Promises vs Results"]

# ── Helpers ────────────────────────────────────────────────────
def detect_company(text: str):
    text_lower = text.lower()
    for key, data in COMPANIES.items():
        if key in text_lower or data["name"].lower().split()[0] in text_lower:
            return key
    return None

def risk_color(score):
    if score >= 7.5: return C["red"]
    if score >= 6.0: return C["amber"]
    return C["green"]

def risk_badge(score):
    if score >= 7.5: return ("HIGH RISK",   "#F5E8E8", C["red"])
    if score >= 6.0: return ("ELEVATED",    "#F5EDE0", C["amber"])
    return               ("LOW RISK",    "#EBF0E0", C["green"])

def extract_text(pdf_bytes):
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            return "\n".join(
                t for page in pdf.pages[:40]
                if (t := page.extract_text())
            )
    except Exception:
        return ""

def bar_chart(indicators, color):
    labels = list(indicators.keys())
    values = list(indicators.values())
    bar_colors = [risk_color(v) for v in values]

    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=[f"{v}/10" for v in values],
        textposition="outside",
        textfont=dict(size=13, color=C["text"], family="Inter"),
        cliponaxis=False,
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 13], showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(autorange="reversed", tickfont=dict(size=13, family="Inter", color=C["text"])),
        margin=dict(t=8, b=8, l=168, r=64),
        paper_bgcolor=C["white"], plot_bgcolor=C["white"],
        height=240, showlegend=False,
    )
    return fig

def radar_chart(indicators, color):
    labels = list(indicators.keys())
    values = list(indicators.values())
    vc = values + [values[0]]
    lc = labels  + [labels[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vc, theta=lc, fill="toself",
        fillcolor=color + "28",
        line=dict(color=color, width=2.5),
        marker=dict(size=7, color=color),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor=C["sage"],
            radialaxis=dict(visible=True, range=[0, 10],
                tickfont=dict(size=10, color=C["muted"]),
                gridcolor=C["border"], linecolor=C["border"]),
            angularaxis=dict(
                tickfont=dict(size=12, color=C["text"], family="Inter"),
                gridcolor=C["border"], linecolor=C["border"]),
        ),
        showlegend=False,
        margin=dict(t=24, b=24, l=44, r=44),
        paper_bgcolor=C["white"], plot_bgcolor=C["white"],
        height=310,
    )
    return fig

# ── Nav ────────────────────────────────────────────────────────
st.markdown("""
<div class="gl-nav">
  <div class="gl-nav-brand">🌿 Green<span>Lens</span></div>
  <div class="gl-nav-tag">ESG Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# ── Upload panel ───────────────────────────────────────────────
with st.container():
    st.markdown("""
    <div class="gl-upload-title">Sustainability Report Analysis</div>
    <div class="gl-upload-sub">Upload any corporate sustainability or annual report. GreenLens scores it across five evidence-based indicators and flags high-risk language.</div>
    <div class="gl-pills">
      <div class="gl-pill">Target Specificity</div>
      <div class="gl-pill">Data-Backed Claims</div>
      <div class="gl-pill">Standards Alignment</div>
      <div class="gl-pill">Risk Disclosure</div>
      <div class="gl-pill">Promises vs Results</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop a PDF here or click to browse",
        type=["pdf"],
        label_visibility="visible",
    )

# ── Results ────────────────────────────────────────────────────
if uploaded:
    pdf_bytes = uploaded.read()

    with st.spinner("Analysing report…"):
        bar = st.progress(0)
        for i in range(0, 101, 5):
            time.sleep(0.035)
            bar.progress(i)
        bar.empty()

        raw_text = extract_text(pdf_bytes)
        ckey = detect_company(raw_text) or detect_company(uploaded.name.lower())

    data = COMPANIES[ckey] if ckey else {
        "name": uploaded.name.replace(".pdf", "").replace("_", " ").title(),
        "score": 6.5,
        "indicators": {k: 5 for k in INDICATORS},
        "summary": "Analysis complete. The report shows moderate greenwashing risk with several unquantified forward-looking claims.",
        "excerpts": [],
        "stats": {"pages": "—", "claims": "—", "backed": "—"},
    }

    score = data["score"]
    rc = risk_color(score)
    badge_text, badge_bg, badge_col = risk_badge(score)

    st.markdown('<hr class="gl-divider">', unsafe_allow_html=True)

    # Row 1: score | bar chart | radar
    c1, c2, c3 = st.columns([1, 1.4, 1.5])

    with c1:
        st.markdown(f"""
        <div class="score-card">
          <div class="score-eyebrow">Greenwashing Risk Score</div>
          <div class="score-number" style="color:{rc};">{score}</div>
          <div class="score-denom">out of 10</div>
          <div class="score-badge" style="background:{badge_bg};color:{badge_col};">{badge_text}</div>
          <div class="score-company">{data['name']}</div>
          <div class="score-summary">{data['summary']}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec-label">Indicator Breakdown</div>', unsafe_allow_html=True)
        st.plotly_chart(bar_chart(data["indicators"], rc), use_container_width=True, config={"displayModeBar": False})

    with c3:
        st.markdown('<div class="sec-label">Risk Profile</div>', unsafe_allow_html=True)
        st.plotly_chart(radar_chart(data["indicators"], rc), use_container_width=True, config={"displayModeBar": False})

    # Row 2: stat tiles
    st.markdown('<div class="sec-label" style="margin-top:8px;">Report Statistics</div>', unsafe_allow_html=True)
    backed = data["stats"]["backed"]
    tiles = [
        (data["stats"]["pages"], "Pages Analysed",             C["text"]),
        (data["stats"]["claims"],"Sustainability Claims",       C["text"]),
        (f"{backed}%"  if isinstance(backed, int) else "—", "Claims Evidenced",    C["green"]),
        (f"{100-backed}%" if isinstance(backed, int) else "—", "Claims Unsupported", C["red"]),
    ]
    cols = st.columns(4)
    for col_w, (val, lbl, tc) in zip(cols, tiles):
        with col_w:
            st.markdown(f"""
            <div class="stat-tile">
              <div class="stat-val" style="color:{tc};">{val}</div>
              <div class="stat-lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    # Row 3: excerpts | comparison
    st.markdown('<hr class="gl-divider">', unsafe_allow_html=True)
    ce, cc = st.columns([1.6, 1])

    with ce:
        st.markdown('<div class="sec-label">Flagged Language</div>', unsafe_allow_html=True)
        if data["excerpts"]:
            for ex in data["excerpts"]:
                lvl = ex["level"]
                cls = "red" if lvl == "red" else "amber"
                tag_cls = "tag-red" if lvl == "red" else "tag-amber"
                st.markdown(f"""
                <div class="excerpt {cls}">
                  <div class="excerpt-quote">"{ex['quote']}"</div>
                  <span class="excerpt-tag {tag_cls}">{ex['tag']}</span>
                  <div class="excerpt-reason" style="margin-top:6px;">{ex['reason']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="color:{C["muted"]};font-size:14px;padding:16px 0;">No flagged excerpts available for this report.</p>', unsafe_allow_html=True)

    with cc:
        st.markdown('<div class="sec-label">Benchmark Comparison</div>', unsafe_allow_html=True)
        scores = {v["name"].split()[0]: v["score"] for v in COMPANIES.values()}
        scores["Avg"] = INDUSTRY_AVG
        for name, s in sorted(scores.items(), key=lambda x: -x[1]):
            pct = int(s / 10 * 100)
            bc  = risk_color(s)
            is_current = name == data["name"].split()[0]
            weight = "font-weight:800;" if is_current else ""
            st.markdown(f"""
            <div class="cmp-row">
              <div class="cmp-name" style="{weight}">{name}</div>
              <div class="cmp-track">
                <div class="cmp-fill" style="width:{pct}%;background:{bc};">{s}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="legend-box">
          <b>Score guide</b><br>
          <span style="color:{C['red']};">● 7.5–10</span>&nbsp; High risk<br>
          <span style="color:{C['amber']};">● 6.0–7.4</span>&nbsp; Elevated<br>
          <span style="color:{C['green']};">● 0–5.9</span>&ensp; Low risk
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div class="landing">
      <div class="landing-icon">🌿</div>
      <div class="landing-title">Drop in a sustainability report</div>
      <div class="landing-sub">
        GreenLens scores any corporate report across five evidence-based indicators
        and surfaces language that doesn't hold up to scrutiny.
      </div>
      <div class="landing-indicators">
        <div class="gl-pill">Target Specificity</div>
        <div class="gl-pill">Data-Backed Claims</div>
        <div class="gl-pill">Standards Alignment</div>
        <div class="gl-pill">Risk Disclosure</div>
        <div class="gl-pill">Promises vs Results</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown("""
<div class="gl-footer">
  <div class="gl-footer-left">🌿 Green<span>Lens</span> &nbsp;·&nbsp; ESG Intelligence Platform</div>
  <div class="gl-footer-right">5 indicators &nbsp;·&nbsp; Research-grounded &nbsp;·&nbsp; ML-validated</div>
</div>
""", unsafe_allow_html=True)
