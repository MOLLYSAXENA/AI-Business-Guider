import streamlit as st
import google.generativeai as genai

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Business Guider",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Reset & base ---- */
[data-testid="stAppViewContainer"] { background: #f8fafc; }
[data-testid="block-container"] { padding: 2rem 3rem 4rem; max-width: 860px; margin: auto; }

/* ---- Typography ---- */
h1 { font-size: 1.65rem !important; font-weight: 600 !important; color: #0f172a !important; }
h3 { font-size: 1rem !important; font-weight: 600 !important; color: #1e293b !important; margin-bottom: .25rem !important; }

/* ---- Form card ---- */
.form-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 28px;
    box-shadow: 0 1px 4px rgba(0,0,0,.04);
}

/* ---- Input labels ---- */
label { font-size: 0.82rem !important; font-weight: 600 !important; color: #64748b !important; letter-spacing: .03em; }

/* ---- Streamlit widgets ---- */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
textarea {
    border-radius: 8px !important;
    border-color: #e2e8f0 !important;
    font-size: 0.9rem !important;
}
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within,
textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.12) !important;
}

/* ---- Primary button ---- */
.stButton > button[kind="primary"] {
    background: #2563eb !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    padding: 0.65rem 1.5rem !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: .02em;
    box-shadow: 0 2px 8px rgba(37,99,235,.25);
    transition: opacity .2s, transform .15s;
}
.stButton > button[kind="primary"]:hover { opacity: .9; transform: translateY(-1px); }
.stButton > button[kind="primary"]:active { transform: scale(.98); }

/* ---- Download button ---- */
.stDownloadButton > button {
    border-radius: 9px !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    border-color: #e2e8f0 !important;
    color: #334155 !important;
    background: #fff !important;
}

/* ---- Pipeline node cards ---- */
.node-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #cbd5e1;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    transition: border-left-color .3s;
}
.node-card.active  { border-left-color: #3b82f6; background: #eff6ff; }
.node-card.done    { border-left-color: #22c55e; background: #f0fdf4; }

.node-title {
    font-weight: 600;
    font-size: 0.9rem;
    color: #1e293b;
    display: flex;
    align-items: center;
    gap: 8px;
}
.node-sub  { font-size: 0.8rem; color: #64748b; margin-top: 4px; }
.node-ok   { font-size: 0.8rem; color: #16a34a; margin-top: 4px; font-weight: 500; }

/* ---- Tabs ---- */
button[data-baseweb="tab"] {
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    color: #64748b !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #2563eb !important;
    border-bottom-color: #2563eb !important;
}

/* ---- Result content ---- */
.result-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 22px 26px;
    font-size: 0.9rem;
    line-height: 1.8;
    color: #1e293b;
}

/* ---- Divider ---- */
hr { border: none; border-top: 1px solid #e2e8f0 !important; margin: 1.8rem 0 !important; }

/* ---- Success banner ---- */
.success-banner {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 10px;
    padding: 12px 18px;
    color: #15803d;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ---- Validation warning ---- */
.warn-box {
    background: #fefce8;
    border: 1px solid #fde047;
    border-radius: 10px;
    padding: 12px 18px;
    color: #854d0e;
    font-size: 0.875rem;
    margin-bottom: 14px;
}

/* ---- Section heading ---- */
.section-heading {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: .08em;
    color: #94a3b8;
    text-transform: uppercase;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


# ── API setup ─────────────────────────────────────────────────────────────────
api_key = st.secrets.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ GEMINI_API_KEY is missing from Streamlit Secrets.")
    st.stop()

MODEL = "gemini-2.5-flash"


# ── Agent functions ───────────────────────────────────────────────────────────
def agent_market(field: str, audience: str) -> str:
    m = genai.GenerativeModel(MODEL)
    return m.generate_content(f"""
You are a startup market analyst. Industry: '{field}'. Target audience: '{audience}'.
Identify exactly 3 high-impact consumer pain points and underserved market gaps.
Format as bullet points. Max 2 concise sentences per point. No intro/outro text.
""").text


def agent_risk(field: str, budget: str, market_ctx: str) -> str:
    m = genai.GenerativeModel(MODEL)
    return m.generate_content(f"""
You are a venture capital risk auditor. Industry: '{field}'. Budget tier: '{budget}'.
Market context: {market_ctx}
State exactly 3 critical risks or financial traps that cause early startup failure.
Max 2 sentences each. No intro/outro text.
""").text


def agent_roadmap(idea: str, market_ctx: str, risk_ctx: str) -> str:
    m = genai.GenerativeModel(MODEL)
    return m.generate_content(f"""
You are an incubator director. Startup concept: '{idea}'.
Market context: {market_ctx}
Risks: {risk_ctx}
Create a Month 1 execution playbook broken into Weeks 1–4.
Use "### Week N — Title" headers. One clear action item per week, max 20 words each.
""").text


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 💼 AI Business Guider")
st.markdown(
    "<p style='color:#64748b; font-size:0.9rem; margin-top:-8px; margin-bottom:20px;'>"
    "Map market opportunities, de-risk your finances, and generate a week-by-week launch playbook."
    "</p>",
    unsafe_allow_html=True,
)


# ── Input form ────────────────────────────────────────────────────────────────
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Startup details</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    field = st.selectbox(
        "Industry vertical",
        ["Technology & Software", "Healthcare & Medical Technology",
         "Education Technology", "E-Commerce", "FoodTech & Hospitality"],
    )
    budget = st.selectbox("Starting budget", ["Small Budget", "Medium Budget", "Large Budget"])

with col_b:
    audience = st.text_input(
        "Target customers",
        placeholder="e.g., college students, busy parents, SaaS teams…",
    )
    idea = st.text_area(
        "Startup concept",
        height=110,
        placeholder="e.g., An AI-driven gamified math learning platform for primary school students…",
    )

st.markdown("<br>", unsafe_allow_html=True)
run = st.button("🚀  Generate Strategic Blueprint", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


# ── Pipeline ──────────────────────────────────────────────────────────────────
if run:
    if not audience.strip() or not idea.strip():
        st.markdown(
            '<div class="warn-box">⚠️ Please fill in both <strong>Target customers</strong>'
            ' and <strong>Startup concept</strong> before running.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    st.markdown("---")
    st.markdown('<div class="section-heading">Live processing</div>', unsafe_allow_html=True)

    # Placeholders for the three nodes
    ph1 = st.empty()
    ph2 = st.empty()
    ph3 = st.empty()

    def node_html(icon, title, sub, state="idle"):
        cls = {"idle": "", "active": "active", "done": "done"}.get(state, "")
        sub_cls = "node-ok" if state == "done" else "node-sub"
        tick = "✓ " if state == "done" else ("⏳ " if state == "active" else "")
        return (
            f'<div class="node-card {cls}">'
            f'<div class="node-title">{icon} {title}</div>'
            f'<div class="{sub_cls}">{tick}{sub}</div>'
            f"</div>"
        )

    # Node 1 — active
    ph1.markdown(node_html("🔍", "Market intelligence analyst",
                            "Mapping consumer pain points and market gaps…", "active"),
                 unsafe_allow_html=True)
    ph2.markdown(node_html("💰", "Capital & venture risk auditor", "Waiting…"), unsafe_allow_html=True)
    ph3.markdown(node_html("📋", "Incubation roadmap director", "Waiting…"), unsafe_allow_html=True)

    try:
        res1 = agent_market(field, audience)
    except Exception as e:
        st.error(f"Agent 1 error: {e}")
        st.stop()

    ph1.markdown(node_html("🔍", "Market intelligence analyst",
                            "Market gaps successfully mapped.", "done"), unsafe_allow_html=True)

    # Node 2 — active
    ph2.markdown(node_html("💰", "Capital & venture risk auditor",
                            "Auditing financial risks and failure vectors…", "active"),
                 unsafe_allow_html=True)
    try:
        res2 = agent_risk(field, budget, res1)
    except Exception as e:
        st.error(f"Agent 2 error: {e}")
        st.stop()

    ph2.markdown(node_html("💰", "Capital & venture risk auditor",
                            "Critical risk vectors identified.", "done"), unsafe_allow_html=True)

    # Node 3 — active
    ph3.markdown(node_html("📋", "Incubation roadmap director",
                            "Building week-by-week action plan…", "active"),
                 unsafe_allow_html=True)
    try:
        res3 = agent_roadmap(idea, res1, res2)
    except Exception as e:
        st.error(f"Agent 3 error: {e}")
        st.stop()

    ph3.markdown(node_html("📋", "Incubation roadmap director",
                            "Action roadmap compiled.", "done"), unsafe_allow_html=True)


    # ── Results ───────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        '<div class="success-banner">✨ Strategic blueprint compiled successfully!</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["🔍 Market gaps & insights", "🚨 Risk & runway audit", "📅 4-week roadmap"])

    with tab1:
        st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
        st.markdown(res1)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
        st.markdown(res2)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown(f'<div class="result-box">', unsafe_allow_html=True)
        st.markdown(res3)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Download ──────────────────────────────────────────────────────────────
    report = (
        "AI BUSINESS GUIDER — STRATEGIC BLUEPRINT\n"
        + "=" * 44 + "\n\n"
        "[MARKET GAPS & INSIGHTS]\n" + res1 + "\n\n"
        "[RISK & RUNWAY AUDIT]\n" + res2 + "\n\n"
        "[4-WEEK ACTION ROADMAP]\n" + res3
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="📥  Download full strategy report",
        data=report,
        file_name="business_blueprint.txt",
        mime="text/plain",
        use_container_width=True,
    )
