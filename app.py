import streamlit as st
import google.generativeai as genai

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Business Guider",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f8fafc; }
[data-testid="block-container"] { padding: 2rem 3rem 4rem; max-width: 920px; margin: auto; }

h1 { font-size: 1.65rem !important; font-weight: 600 !important; color: #0f172a !important; }
h3 { font-size: 1rem !important; font-weight: 600 !important; color: #1e293b !important; margin-bottom:.25rem !important; }

.form-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 28px 32px; margin-bottom: 28px; box-shadow: 0 1px 4px rgba(0,0,0,.04);
}
label { font-size: 0.82rem !important; font-weight: 600 !important; color: #64748b !important; letter-spacing:.03em; }

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
textarea {
    border-radius: 8px !important; border-color: #e2e8f0 !important; font-size: 0.9rem !important;
}
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within,
textarea:focus {
    border-color: #3b82f6 !important; box-shadow: 0 0 0 3px rgba(59,130,246,.12) !important;
}

.stButton > button[kind="primary"] {
    background: #2563eb !important; color: #fff !important; border: none !important;
    border-radius: 9px !important; padding: 0.65rem 1.5rem !important;
    font-size: 0.9rem !important; font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(37,99,235,.25); transition: opacity .2s, transform .15s;
}
.stButton > button[kind="primary"]:hover { opacity:.9; transform:translateY(-1px); }
.stButton > button[kind="primary"]:active { transform:scale(.98); }

.stDownloadButton > button {
    border-radius: 9px !important; font-size: 0.875rem !important;
    font-weight: 500 !important; border-color: #e2e8f0 !important;
    color: #334155 !important; background: #fff !important;
}

.node-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #cbd5e1;
    border-radius: 10px; padding: 14px 18px; margin-bottom: 10px;
}
.node-card.active { border-left-color: #3b82f6; background: #eff6ff; }
.node-card.done   { border-left-color: #22c55e; background: #f0fdf4; }
.node-title { font-weight: 600; font-size: 0.9rem; color: #1e293b; }
.node-sub { font-size: 0.8rem; color: #64748b; margin-top: 4px; }
.node-ok  { font-size: 0.8rem; color: #16a34a; margin-top: 4px; font-weight: 500; }

button[data-baseweb="tab"] { font-size: 0.875rem !important; font-weight: 600 !important; color: #64748b !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #2563eb !important; border-bottom-color: #2563eb !important; }

.result-box {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 22px 26px; font-size: 0.9rem; line-height: 1.8; color: #1e293b;
}
hr { border: none; border-top: 1px solid #e2e8f0 !important; margin: 1.8rem 0 !important; }

.success-banner {
    background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px;
    padding: 12px 18px; color: #15803d; font-size: 0.875rem; font-weight: 600;
    margin-bottom: 18px;
}
.warn-box {
    background: #fefce8; border: 1px solid #fde047; border-radius: 10px;
    padding: 12px 18px; color: #854d0e; font-size: 0.875rem; margin-bottom: 14px;
}
.section-heading {
    font-size: 0.75rem; font-weight: 700; letter-spacing:.08em;
    color: #94a3b8; text-transform: uppercase; margin-bottom: 12px;
}

/* Budget summary cards */
.budget-grid { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 8px; }
.budget-card {
    flex: 1; min-width: 140px;
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 14px 16px;
}
.budget-card .bc-label { font-size: 0.72rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing:.06em; }
.budget-card .bc-value { font-size: 1.15rem; font-weight: 700; color: #1e293b; margin-top: 4px; }
.budget-card .bc-sub   { font-size: 0.78rem; color: #64748b; margin-top: 2px; }
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

def agent_market(field, audience):
    m = genai.GenerativeModel(MODEL)
    return m.generate_content(f"""
You are a friendly startup advisor. Write in very simple, everyday English — like you're explaining to a friend.
Industry: '{field}'. Target customers: '{audience}'.

Give exactly 3 market gaps or customer pain points.

Format each like this:
### 🔍 Gap [N]: [Short title]
- **What the problem is:** One plain sentence.
- **Why it matters:** One plain sentence.
- **Opportunity:** One plain sentence about what a startup can do here.

No jargon. No fancy words. Keep it easy to read.
""").text


def agent_risk(field, budget, market_ctx):
    m = genai.GenerativeModel(MODEL)
    return m.generate_content(f"""
You are a friendly business risk advisor. Write in very simple English — no jargon.
Industry: '{field}'. Budget level: '{budget}'.
Market context: {market_ctx}

Give exactly 3 risks a startup in this space might face.

Format each like this:
### ⚠️ Risk [N]: [Short title]
- **What could go wrong:** One plain sentence.
- **Why this happens:** One plain sentence.
- **How to avoid it:** One plain, actionable sentence.

Keep it simple and easy to understand.
""").text


def agent_roadmap(idea, market_ctx, risk_ctx):
    m = genai.GenerativeModel(MODEL)
    return m.generate_content(f"""
You are a startup coach. Write in very simple English.
Startup idea: '{idea}'
Market context: {market_ctx}
Risks to watch: {risk_ctx}

Create a Month 1 action plan broken into 4 weeks.

For EACH week use this format:
### 📅 Week [N] — [Short week title]
| Task | Why it matters | Time needed |
|------|---------------|-------------|
| [task 1] | [simple reason] | [e.g. 2 days] |
| [task 2] | [simple reason] | [e.g. 1 day] |
| [task 3] | [simple reason] | [e.g. 3 days] |

**Goal for the week:** One sentence on what success looks like.

Keep language simple. Use action verbs. Be specific.
""").text


def agent_budget(field, budget, idea, market_ctx):
    m = genai.GenerativeModel(MODEL)
    return m.generate_content(f"""
You are a friendly financial advisor for startups. Write in very simple, clear English.
Industry: '{field}'. Budget level: '{budget}'. Startup idea: '{idea}'.
Market context: {market_ctx}

First, based on the budget level, estimate a realistic total starting budget in USD:
- Small Budget = $1,000 – $5,000
- Medium Budget = $5,000 – $25,000
- Large Budget = $25,000 – $100,000

Pick a specific number within the right range and use it throughout.

Output the following sections:

### 💵 Total Estimated Budget
State the total in one line, e.g. "Your estimated starting budget: **$8,000**"

### 📊 How to Spend It (Budget Breakdown)
| Category | Estimated Cost | % of Budget | What it covers |
|----------|---------------|-------------|----------------|
| [category] | $[amount] | [X]% | [plain description] |
(Include 5–7 rows. Make sure amounts add up to the total.)

### 💡 Money-Saving Tips
Give exactly 3 bullet points. Each tip should be practical and simple.
- 💰 **Tip:** [what to do and why it saves money]

### 🚀 When Will You Need More Money?
- **Month [N]:** [Simple sentence about when/why you'd need to raise or reinvest]

Keep everything in plain English. No complicated finance words.
""").text


# ── Helper ────────────────────────────────────────────────────────────────────
def node_html(icon, title, sub, state="idle"):
    cls  = {"idle": "", "active": "active", "done": "done"}.get(state, "")
    scls = "node-ok" if state == "done" else "node-sub"
    tick = "✓ " if state == "done" else ("⏳ " if state == "active" else "")
    return (
        f'<div class="node-card {cls}">'
        f'<div class="node-title">{icon} {title}</div>'
        f'<div class="{scls}">{tick}{sub}</div>'
        f"</div>"
    )


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 💼 AI Business Guider")
st.markdown(
    "<p style='color:#64748b;font-size:0.9rem;margin-top:-8px;margin-bottom:20px;'>"
    "Get a simple, deep guide — market gaps, risks, budget breakdown, and a week-by-week action plan."
    "</p>",
    unsafe_allow_html=True,
)

# ── Form ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Your startup details</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)
with col_a:
    field = st.selectbox(
        "Industry",
        ["Technology & Software", "Healthcare & Medical Technology",
         "Education Technology", "E-Commerce", "FoodTech & Hospitality"],
    )
    budget = st.selectbox("Starting budget", ["Small Budget", "Medium Budget", "Large Budget"])

with col_b:
    audience = st.text_input("Who are your customers?",
                              placeholder="e.g., college students, busy parents, SaaS teams…")
    idea = st.text_area("What is your startup idea?", height=110,
                        placeholder="e.g., AI-driven gamified math learning for primary school students…")

st.markdown("<br>", unsafe_allow_html=True)
run = st.button("🚀  Generate Full Business Guide", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)


# ── Pipeline ──────────────────────────────────────────────────────────────────
if run:
    if not audience.strip() or not idea.strip():
        st.markdown(
            '<div class="warn-box">⚠️ Please fill in both <b>Who are your customers?</b>'
            ' and <b>What is your startup idea?</b> before running.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    st.markdown("---")
    st.markdown('<div class="section-heading">Live processing — 4 AI agents running</div>',
                unsafe_allow_html=True)

    ph1, ph2, ph3, ph4 = st.empty(), st.empty(), st.empty(), st.empty()

    # ── Agent 1: Market ───────────────────────────────────────────────────────
    ph1.markdown(node_html("🔍", "Market analyst", "Finding market gaps and customer problems…", "active"),
                 unsafe_allow_html=True)
    ph2.markdown(node_html("⚠️", "Risk advisor", "Waiting…"), unsafe_allow_html=True)
    ph3.markdown(node_html("💵", "Budget planner", "Waiting…"), unsafe_allow_html=True)
    ph4.markdown(node_html("📋", "Roadmap coach", "Waiting…"), unsafe_allow_html=True)

    try:
        res1 = agent_market(field, audience)
    except Exception as e:
        st.error(f"Agent 1 error: {e}"); st.stop()
    ph1.markdown(node_html("🔍", "Market analyst", "Market gaps mapped.", "done"), unsafe_allow_html=True)

    # ── Agent 2: Risk ─────────────────────────────────────────────────────────
    ph2.markdown(node_html("⚠️", "Risk advisor", "Finding risks and how to avoid them…", "active"),
                 unsafe_allow_html=True)
    try:
        res2 = agent_risk(field, budget, res1)
    except Exception as e:
        st.error(f"Agent 2 error: {e}"); st.stop()
    ph2.markdown(node_html("⚠️", "Risk advisor", "Risks identified.", "done"), unsafe_allow_html=True)

    # ── Agent 3: Budget ───────────────────────────────────────────────────────
    ph3.markdown(node_html("💵", "Budget planner", "Building your budget breakdown…", "active"),
                 unsafe_allow_html=True)
    try:
        res3 = agent_budget(field, budget, idea, res1)
    except Exception as e:
        st.error(f"Agent 3 error: {e}"); st.stop()
    ph3.markdown(node_html("💵", "Budget planner", "Budget plan ready.", "done"), unsafe_allow_html=True)

    # ── Agent 4: Roadmap ──────────────────────────────────────────────────────
    ph4.markdown(node_html("📋", "Roadmap coach", "Building your week-by-week action plan…", "active"),
                 unsafe_allow_html=True)
    try:
        res4 = agent_roadmap(idea, res1, res2)
    except Exception as e:
        st.error(f"Agent 4 error: {e}"); st.stop()
    ph4.markdown(node_html("📋", "Roadmap coach", "Action plan compiled.", "done"), unsafe_allow_html=True)

    # ── Results ───────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="success-banner">✨ Your full business guide is ready!</div>',
                unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Market gaps",
        "⚠️ Risks & how to avoid",
        "💵 Budget breakdown",
        "📅 4-week action plan",
    ])

    with tab1:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(res1)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(res2)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(res3)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(res4)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Download ──────────────────────────────────────────────────────────────
    report = (
        "AI BUSINESS GUIDER — FULL GUIDE\n" + "=" * 44 + "\n\n"
        f"Industry: {field} | Budget: {budget}\n"
        f"Customers: {audience}\n"
        f"Idea: {idea}\n\n"
        "[1. MARKET GAPS & OPPORTUNITIES]\n" + res1 + "\n\n"
        "[2. RISKS & HOW TO AVOID THEM]\n" + res2 + "\n\n"
        "[3. BUDGET BREAKDOWN]\n" + res3 + "\n\n"
        "[4. 4-WEEK ACTION PLAN]\n" + res4
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="📥  Download full business guide",
        data=report,
        file_name="business_guide.txt",
        mime="text/plain",
        use_container_width=True,
    )
