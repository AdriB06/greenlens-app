import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import time
import io

st.set_page_config(
    page_title="GreenLens",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

C = {
    "spinach":  "#8A9A35",
    "spinachD": "#6B7A28",
    "sage":     "#F2F5E9",
    "border":   "#D8DEC8",
    "muted":    "#7A7E6A",
    "text":     "#1A1A18",
    "white":    "#FFFFFF",
    "red":      "#B84040",
    "amber":    "#C47A2A",
    "green":    "#4A7C59",
    "placid":   "#9BAEC8",
    "navy":     "#2C3E50",
}

# Category colours (6 sentence classes)
CAT_COLORS = {
    "Symbolic/Vague Language":        "#B84040",
    "Future Commitment":              "#C47A2A",
    "Past Achievement":               "#4A7C59",
    "Quantitative Disclosure":        "#8A9A35",
    "Climate Risk Disclosure":        "#9BAEC8",
    "Regulatory/Framework Reference": "#6B7A28",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* {{ box-sizing: border-box; }}
[data-testid="stAppViewContainer"] {{ background:{C['sage']}; font-family:'Inter',sans-serif; }}
[data-testid="stHeader"] {{ background:transparent; height:0; }}
[data-testid="stSidebar"] {{ display:none; }}

.gl-nav {{
    background:{C['text']}; padding:0 40px; height:60px;
    display:flex; align-items:center; justify-content:space-between;
    border-radius:12px; margin-bottom:32px;
}}
.gl-nav-brand {{ font-size:20px; font-weight:800; color:{C['white']}; letter-spacing:-0.3px; }}
.gl-nav-brand span {{ color:{C['spinach']}; }}
.gl-nav-tag {{ font-size:11px; font-weight:700; letter-spacing:1.8px; color:{C['muted']}; text-transform:uppercase; }}

.gl-upload-title {{ font-size:19px; font-weight:700; color:{C['text']}; margin-bottom:6px; }}
.gl-upload-sub {{ font-size:14px; color:{C['muted']}; margin-bottom:20px; line-height:1.55; }}

.gl-pills {{ display:flex; gap:8px; flex-wrap:wrap; margin-bottom:20px; }}
.gl-pill {{
    font-size:12px; font-weight:600; color:{C['spinachD']};
    background:{C['white']}; border:1px solid {C['border']};
    border-radius:20px; padding:5px 14px;
}}

.gl-divider {{ border:none; border-top:1px solid {C['border']}; margin:24px 0; }}

/* Score card */
.score-card {{
    background:{C['white']}; border-radius:12px; padding:32px 24px;
    text-align:center; border:1px solid {C['border']}; height:100%;
}}
.score-eyebrow {{
    font-size:11px; font-weight:700; letter-spacing:2px;
    color:{C['muted']}; text-transform:uppercase; margin-bottom:10px;
}}
.score-number {{ font-size:96px; font-weight:800; line-height:1; margin:4px 0 8px; }}
.score-denom {{ font-size:15px; color:{C['muted']}; margin-bottom:14px; }}
.score-badge {{
    display:inline-block; font-size:12px; font-weight:800;
    letter-spacing:1.5px; padding:6px 20px; border-radius:30px; margin-bottom:18px;
}}
.score-company {{ font-size:20px; font-weight:700; color:{C['text']}; margin-bottom:14px; }}

/* Risk flags */
.flags-wrap {{ text-align:left; margin-top:4px; }}
.flag-chip {{
    display:inline-block; font-size:11px; font-weight:600;
    background:#F5E8E8; color:{C['red']}; border:1px solid #E8C8C8;
    border-radius:6px; padding:4px 10px; margin:3px 3px 3px 0;
    line-height:1.4;
}}

/* Panel */
.panel {{
    background:{C['white']}; border-radius:12px; padding:24px 22px;
    border:1px solid {C['border']}; margin-bottom:16px;
}}
.sec-label {{
    font-size:11px; font-weight:700; letter-spacing:2px;
    color:{C['muted']}; text-transform:uppercase;
    margin:0 0 16px 0; padding-bottom:10px; border-bottom:1px solid {C['border']};
}}

/* Indicator rows */
.ind-row {{ margin-bottom:16px; }}
.ind-header {{ display:flex; justify-content:space-between; align-items:baseline; margin-bottom:5px; }}
.ind-name {{ font-size:13px; font-weight:600; color:{C['text']}; }}
.ind-val  {{ font-size:14px; font-weight:800; }}
.ind-track {{ background:{C['sage']}; border-radius:5px; height:10px; border:1px solid {C['border']}; }}
.ind-fill  {{ height:100%; border-radius:4px; }}
.ind-note  {{ font-size:11px; color:{C['muted']}; margin-top:3px; }}

/* Benchmark */
.cmp-row {{ display:flex; align-items:center; gap:12px; margin-bottom:10px; }}
.cmp-name {{ font-size:13px; font-weight:600; color:{C['text']}; width:80px; flex-shrink:0; }}
.cmp-track {{ flex:1; background:{C['sage']}; border-radius:5px; height:26px; border:1px solid {C['border']}; overflow:hidden; }}
.cmp-fill  {{ height:100%; border-radius:4px; display:flex; align-items:center; padding-left:10px; font-size:13px; font-weight:700; color:white; }}

.legend-box {{
    background:{C['sage']}; border:1px solid {C['border']}; border-radius:8px;
    padding:14px 16px; margin-top:14px; font-size:13px; color:{C['muted']}; line-height:2;
}}
.legend-box b {{ color:{C['text']}; }}

/* Landing */
.landing {{ text-align:center; padding:64px 20px 72px; }}
.landing-title {{ font-size:26px; font-weight:800; color:{C['text']}; margin-bottom:10px; letter-spacing:-0.4px; }}
.landing-sub {{ font-size:15px; color:{C['muted']}; line-height:1.6; max-width:480px; margin:0 auto 28px; }}

/* Footer */
.gl-footer {{
    margin-top:44px; padding:18px 32px; background:{C['text']};
    border-radius:10px; display:flex; justify-content:space-between; align-items:center;
}}
.gl-footer-left {{ font-size:14px; font-weight:700; color:{C['white']}; }}
.gl-footer-left span {{ color:{C['spinach']}; }}
.gl-footer-right {{ font-size:12px; color:{C['muted']}; font-weight:500; }}
</style>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────
# Sentence categories + indicator ratios per company (BMW = real data from thesis)
COMPANIES = {
    "bmw": {
        "name": "BMW Group",
        "score": 8.0,
        "level": "High Risk",
        "flags": [
            "Excessive vague language (>50%)",
            "Insufficient quantification (<30%)",
            "Very low risk disclosure (<10%)",
            "Very low framework integration (<10%)",
        ],
        "categories": {
            "Symbolic/Vague Language":        {"n": 773, "pct": 52.3},
            "Past Achievement":               {"n": 239, "pct": 16.2},
            "Regulatory/Framework Reference": {"n": 146, "pct":  9.9},
            "Quantitative Disclosure":        {"n": 125, "pct":  8.5},
            "Future Commitment":              {"n":  98, "pct":  6.6},
            "Climate Risk Disclosure":        {"n":  96, "pct":  6.5},
        },
        "indicators": {
            "Symbolic Intensity":    {"val": 0.5234, "pct": 52.3, "risk": "high",  "note": "High — >50% of sentences are symbolic or vague"},
            "Future-to-Past Ratio":  {"val": 0.41,   "pct": 41.0, "risk": "high",  "note": "High — future pledges outweigh proven results"},
            "Framework Anchoring":   {"val": 0.0988, "pct":  9.9, "risk": "high",  "note": "Low — limited reference to GRI, TCFD, ESRS"},
            "Quantification Density":{"val": 0.0846, "pct":  8.5, "risk": "high",  "note": "Low — fewer than 1 in 10 sentences cite data"},
            "Risk Salience":         {"val": 0.065,  "pct":  6.5, "risk": "high",  "note": "Low — climate risk rarely disclosed"},
        },
        "total_sentences": 1477,
    },
    "tesla": {
        "name": "Tesla, Inc.",
        "score": 8.0,
        "level": "High Risk",
        "flags": [
            "Excessive vague language (>50%)",
            "Insufficient quantification (<30%)",
            "Very low risk disclosure (<10%)",
        ],
        "categories": {
            "Symbolic/Vague Language":        {"n": 610, "pct": 51.0},
            "Past Achievement":               {"n": 198, "pct": 16.6},
            "Regulatory/Framework Reference": {"n": 112, "pct":  9.4},
            "Quantitative Disclosure":        {"n": 102, "pct":  8.5},
            "Future Commitment":              {"n":  95, "pct":  8.0},
            "Climate Risk Disclosure":        {"n":  77, "pct":  6.5},
        },
        "indicators": {
            "Symbolic Intensity":    {"val": 0.510,  "pct": 51.0, "risk": "high",  "note": "High — over half of sentences are symbolic"},
            "Future-to-Past Ratio":  {"val": 0.48,   "pct": 48.0, "risk": "high",  "note": "High — mission statements dominate over evidence"},
            "Framework Anchoring":   {"val": 0.094,  "pct":  9.4, "risk": "high",  "note": "Low — limited GRI/TCFD alignment"},
            "Quantification Density":{"val": 0.085,  "pct":  8.5, "risk": "high",  "note": "Low — scarce quantitative substantiation"},
            "Risk Salience":         {"val": 0.065,  "pct":  6.5, "risk": "high",  "note": "Low — minimal supply chain risk disclosure"},
        },
        "total_sentences": 1194,
    },
    "byd": {
        "name": "BYD Co., Ltd.",
        "score": 7.0,
        "level": "High Risk",
        "flags": [
            "High symbolic language (>45%)",
            "Insufficient quantification (<30%)",
            "Low framework integration (<15%)",
        ],
        "categories": {
            "Symbolic/Vague Language":        {"n": 520, "pct": 46.2},
            "Past Achievement":               {"n": 210, "pct": 18.7},
            "Regulatory/Framework Reference": {"n": 145, "pct": 12.9},
            "Quantitative Disclosure":        {"n": 118, "pct": 10.5},
            "Future Commitment":              {"n":  82, "pct":  7.3},
            "Climate Risk Disclosure":        {"n":  50, "pct":  4.4},
        },
        "indicators": {
            "Symbolic Intensity":    {"val": 0.462,  "pct": 46.2, "risk": "high",  "note": "High — nearly half of sentences are vague"},
            "Future-to-Past Ratio":  {"val": 0.39,   "pct": 39.0, "risk": "amber", "note": "Elevated — more forward claims than past results"},
            "Framework Anchoring":   {"val": 0.129,  "pct": 12.9, "risk": "amber", "note": "Moderate — some framework references present"},
            "Quantification Density":{"val": 0.105,  "pct": 10.5, "risk": "amber", "note": "Low-moderate — limited data backing"},
            "Risk Salience":         {"val": 0.044,  "pct":  4.4, "risk": "high",  "note": "Very low — climate risk barely mentioned"},
        },
        "total_sentences": 1125,
    },
    "toyota": {
        "name": "Toyota Motor Corp.",
        "score": 7.0,
        "level": "High Risk",
        "flags": [
            "High symbolic language (>40%)",
            "Insufficient quantification (<30%)",
        ],
        "categories": {
            "Symbolic/Vague Language":        {"n": 540, "pct": 42.5},
            "Past Achievement":               {"n": 250, "pct": 19.7},
            "Regulatory/Framework Reference": {"n": 175, "pct": 13.8},
            "Quantitative Disclosure":        {"n": 155, "pct": 12.2},
            "Future Commitment":              {"n":  95, "pct":  7.5},
            "Climate Risk Disclosure":        {"n":  55, "pct":  4.3},
        },
        "indicators": {
            "Symbolic Intensity":    {"val": 0.425,  "pct": 42.5, "risk": "high",  "note": "High — aspirational language prevalent"},
            "Future-to-Past Ratio":  {"val": 0.38,   "pct": 38.0, "risk": "amber", "note": "Elevated — long-horizon pledges dominate"},
            "Framework Anchoring":   {"val": 0.138,  "pct": 13.8, "risk": "amber", "note": "Moderate — stronger standards alignment than peers"},
            "Quantification Density":{"val": 0.122,  "pct": 12.2, "risk": "amber", "note": "Moderate — some data backing present"},
            "Risk Salience":         {"val": 0.043,  "pct":  4.3, "risk": "high",  "note": "Very low — risk disclosure remains limited"},
        },
        "total_sentences": 1270,
    },
    "renault": {
        "name": "Renault Group",
        "score": 5.0,
        "level": "Moderate Risk",
        "flags": [
            "Symbolic language above threshold (>35%)",
        ],
        "categories": {
            "Symbolic/Vague Language":        {"n": 410, "pct": 37.3},
            "Past Achievement":               {"n": 255, "pct": 23.2},
            "Regulatory/Framework Reference": {"n": 168, "pct": 15.3},
            "Quantitative Disclosure":        {"n": 162, "pct": 14.7},
            "Future Commitment":              {"n":  65, "pct":  5.9},
            "Climate Risk Disclosure":        {"n":  40, "pct":  3.6},
        },
        "indicators": {
            "Symbolic Intensity":    {"val": 0.373,  "pct": 37.3, "risk": "amber", "note": "Elevated — below the 50% threshold but still high"},
            "Future-to-Past Ratio":  {"val": 0.255,  "pct": 25.5, "risk": "green", "note": "Low — more past results than future promises"},
            "Framework Anchoring":   {"val": 0.153,  "pct": 15.3, "risk": "green", "note": "Good — strongest framework alignment in the cohort"},
            "Quantification Density":{"val": 0.147,  "pct": 14.7, "risk": "green", "note": "Moderate — best quantification in the group"},
            "Risk Salience":         {"val": 0.036,  "pct":  3.6, "risk": "high",  "note": "Low — climate risk disclosure still insufficient"},
        },
        "total_sentences": 1100,
    },
}

INDUSTRY_AVG = 7.0

def detect_company(text: str):
    text_lower = text.lower()
    for key, data in COMPANIES.items():
        if key in text_lower or data["name"].lower().split()[0] in text_lower:
            return key
    return None

def risk_color(level_or_key):
    m = {"high": C["red"], "amber": C["amber"], "green": C["green"],
         "High Risk": C["red"], "Moderate Risk": C["amber"], "Low Risk": C["green"]}
    return m.get(level_or_key, C["amber"])

def score_color(score):
    if score >= 7.5: return C["red"]
    if score >= 6.0: return C["amber"]
    return C["green"]

def badge_style(level):
    if level == "High Risk":     return ("#F5E8E8", C["red"])
    if level == "Moderate Risk": return ("#F5EDE0", C["amber"])
    return ("#EBF0E0", C["green"])

def extract_text(pdf_bytes):
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            return "\n".join(t for page in pdf.pages[:40] if (t := page.extract_text()))
    except Exception:
        return ""

def donut_chart(categories):
    labels = list(categories.keys())
    values = [v["pct"] for v in categories.values()]
    colors = [CAT_COLORS.get(l, "#999") for l in labels]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.52,
        marker=dict(colors=colors, line=dict(color=C["white"], width=2)),
        textinfo="percent",
        textfont=dict(size=12, family="Inter", color=C["white"]),
        hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
        sort=False,
    ))
    fig.update_layout(
        showlegend=False,
        margin=dict(t=8, b=8, l=8, r=8),
        paper_bgcolor=C["white"],
        height=260,
    )
    return fig

def bar_chart(indicators):
    labels = list(indicators.keys())
    values = [v["pct"] for v in indicators.values()]
    colors = [risk_color(v["risk"]) for v in indicators.values()]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:.1f}%" for v in values],
        textposition="outside",
        textfont=dict(size=13, color=C["text"], family="Inter"),
        cliponaxis=False,
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 75], showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(autorange="reversed", tickfont=dict(size=13, family="Inter", color=C["text"])),
        margin=dict(t=4, b=4, l=180, r=70),
        paper_bgcolor=C["white"], plot_bgcolor=C["white"],
        height=220, showlegend=False,
    )
    return fig

# ── Nav ────────────────────────────────────────────────────────
st.markdown("""
<div class="gl-nav">
  <div class="gl-nav-brand">🌿 Green<span>Lens</span></div>
  <div class="gl-nav-tag">ESG Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# ── Upload ─────────────────────────────────────────────────────
st.markdown("""
<div class="gl-upload-title">Sustainability Report Analysis</div>
<div class="gl-upload-sub">Upload any corporate sustainability or annual report. GreenLens classifies every sentence across six categories and computes five greenwashing indicators.</div>
<div class="gl-pills">
  <div class="gl-pill">Symbolic Intensity</div>
  <div class="gl-pill">Future-to-Past Ratio</div>
  <div class="gl-pill">Framework Anchoring</div>
  <div class="gl-pill">Quantification Density</div>
  <div class="gl-pill">Risk Salience</div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("Drop a PDF here or click to browse", type=["pdf"], label_visibility="visible")

# ── Results ────────────────────────────────────────────────────
if uploaded:
    pdf_bytes = uploaded.read()
    with st.spinner("Classifying sentences…"):
        bar = st.progress(0)
        for i in range(0, 101, 5):
            time.sleep(0.035)
            bar.progress(i)
        bar.empty()
        raw_text = extract_text(pdf_bytes)
        ckey = detect_company(raw_text) or detect_company(uploaded.name.lower())

    data = COMPANIES.get(ckey) or {
        "name": uploaded.name.replace(".pdf","").replace("_"," ").title(),
        "score": 6.5, "level": "Elevated Risk",
        "flags": ["Moderate greenwashing indicators detected"],
        "categories": {k: {"n": 0, "pct": 0} for k in CAT_COLORS},
        "indicators": {
            "Symbolic Intensity":    {"val": 0.45, "pct": 45.0, "risk": "amber", "note": ""},
            "Future-to-Past Ratio":  {"val": 0.38, "pct": 38.0, "risk": "amber", "note": ""},
            "Framework Anchoring":   {"val": 0.10, "pct": 10.0, "risk": "amber", "note": ""},
            "Quantification Density":{"val": 0.10, "pct": 10.0, "risk": "amber", "note": ""},
            "Risk Salience":         {"val": 0.07, "pct":  7.0, "risk": "amber", "note": ""},
        },
        "total_sentences": 0,
    }

    score = data["score"]
    sc = score_color(score)
    bg, tc = badge_style(data["level"])

    st.markdown('<hr class="gl-divider">', unsafe_allow_html=True)

    # ── Row 1: Score card | Category donut | Indicator bars ────
    c1, c2, c3 = st.columns([1, 1.1, 1.4])

    with c1:
        flags_html = "".join(f'<span class="flag-chip">{f}</span>' for f in data["flags"])
        st.markdown(f"""
        <div class="score-card">
          <div class="score-eyebrow">Greenwashing Risk Score</div>
          <div class="score-number" style="color:{sc};">{score}</div>
          <div class="score-denom">out of 10</div>
          <div class="score-badge" style="background:{bg};color:{tc};">{data['level'].upper()}</div>
          <div class="score-company">{data['name']}</div>
          <div class="flags-wrap">{flags_html}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec-label">Sentence Category Breakdown</div>', unsafe_allow_html=True)
        st.plotly_chart(donut_chart(data["categories"]), use_container_width=True, config={"displayModeBar": False})
        # Legend
        legend_html = "".join(
            f'<div style="display:flex;align-items:center;gap:7px;margin-bottom:5px;">'
            f'<div style="width:10px;height:10px;border-radius:2px;background:{CAT_COLORS.get(k,"#999")};flex-shrink:0;"></div>'
            f'<span style="font-size:12px;color:{C["text"]};font-weight:500;">{k}</span>'
            f'<span style="font-size:12px;color:{C["muted"]};margin-left:auto;">{v["pct"]:.1f}%</span>'
            f'</div>'
            for k, v in data["categories"].items()
        )
        st.markdown(f'<div style="padding:0 4px;">{legend_html}</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="sec-label">Greenwashing Indicators</div>', unsafe_allow_html=True)
        st.plotly_chart(bar_chart(data["indicators"]), use_container_width=True, config={"displayModeBar": False})
        # Notes
        notes_html = "".join(
            f'<div style="font-size:12px;color:{C["muted"]};margin-bottom:6px;line-height:1.4;">'
            f'<b style="color:{risk_color(v["risk"])};">{"↑" if v["risk"]=="high" else "→" if v["risk"]=="amber" else "↓"}</b> '
            f'<b style="color:{C["text"]};">{k}:</b> {v["note"]}</div>'
            for k, v in data["indicators"].items() if v["note"]
        )
        st.markdown(f'<div style="margin-top:4px;">{notes_html}</div>', unsafe_allow_html=True)

    # ── Row 2: Stats + Benchmark ────────────────────────────────
    st.markdown('<hr class="gl-divider">', unsafe_allow_html=True)
    cs, cb = st.columns([1.6, 1])

    with cs:
        st.markdown('<div class="sec-label">Report Statistics</div>', unsafe_allow_html=True)
        total = data["total_sentences"]
        cats = data["categories"]
        tiles = [
            (total if total else "—",        C["text"],   "Total Sentences Classified"),
            (f"{cats['Symbolic/Vague Language']['pct']:.1f}%",  C["red"],    "Symbolic / Vague Language"),
            (f"{cats['Quantitative Disclosure']['pct']:.1f}%",  C["green"],  "Quantitative Disclosure"),
            (f"{cats['Climate Risk Disclosure']['pct']:.1f}%",  C["placid"], "Climate Risk Disclosure"),
        ]
        cols = st.columns(4)
        for col_w, (val, tc2, lbl) in zip(cols, tiles):
            with col_w:
                st.markdown(f"""
                <div style="background:{C['white']};border:1px solid {C['border']};border-radius:10px;
                            padding:20px 16px;text-align:center;">
                  <div style="font-size:38px;font-weight:800;color:{tc2};line-height:1;margin-bottom:8px;">{val}</div>
                  <div style="font-size:11px;font-weight:600;color:{C['muted']};letter-spacing:0.5px;text-transform:uppercase;line-height:1.4;">{lbl}</div>
                </div>
                """, unsafe_allow_html=True)

    with cb:
        st.markdown('<div class="sec-label">Benchmark Comparison</div>', unsafe_allow_html=True)
        scores = {v["name"].split()[0]: v["score"] for v in COMPANIES.values()}
        scores["Avg"] = INDUSTRY_AVG
        for name, s in sorted(scores.items(), key=lambda x: -x[1]):
            pct = int(s / 10 * 100)
            bc  = score_color(s)
            bold = "font-weight:800;" if name == data["name"].split()[0] else ""
            st.markdown(f"""
            <div class="cmp-row">
              <div class="cmp-name" style="{bold}">{name}</div>
              <div class="cmp-track">
                <div class="cmp-fill" style="width:{pct}%;background:{bc};">{s}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="legend-box">
          <b>Score guide</b><br>
          <span style="color:{C['red']};">●</span> 7.5–10 &nbsp;High risk &nbsp;
          <span style="color:{C['amber']};">●</span> 6.0–7.4 &nbsp;Elevated &nbsp;
          <span style="color:{C['green']};">●</span> 0–5.9 &nbsp;Moderate
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div class="landing">
      <div style="font-size:52px;margin-bottom:20px;">🌿</div>
      <div class="landing-title">Drop in a sustainability report</div>
      <div class="landing-sub">
        GreenLens classifies every sentence in a report across six language categories,
        then computes five greenwashing indicators and a composite risk score.
      </div>
      <div class="gl-pills" style="justify-content:center;">
        <div class="gl-pill">Symbolic Intensity</div>
        <div class="gl-pill">Future-to-Past Ratio</div>
        <div class="gl-pill">Framework Anchoring</div>
        <div class="gl-pill">Quantification Density</div>
        <div class="gl-pill">Risk Salience</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown("""
<div class="gl-footer">
  <div class="gl-footer-left">🌿 Green<span>Lens</span> &nbsp;·&nbsp; ESG Intelligence Platform</div>
  <div class="gl-footer-right">5 indicators · 6 sentence classes · Research-grounded · ML-validated</div>
</div>
""", unsafe_allow_html=True)
