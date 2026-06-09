import io
import re
import streamlit as st
import google.generativeai as genai

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Business Guider",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f8fafc; }
[data-testid="block-container"] { padding: 2rem 3rem 4rem; max-width: 920px; margin: auto; }
h1 { font-size:1.65rem !important; font-weight:600 !important; color:#0f172a !important; }
h3 { font-size:1rem  !important; font-weight:600 !important; color:#1e293b !important; margin-bottom:.25rem !important; }
.form-card { background:#fff; border:1px solid #e2e8f0; border-radius:14px; padding:28px 32px; margin-bottom:28px; box-shadow:0 1px 4px rgba(0,0,0,.04); }
label { font-size:0.82rem !important; font-weight:600 !important; color:#64748b !important; letter-spacing:.03em; }
div[data-baseweb="select"]>div, div[data-baseweb="input"]>div, textarea { border-radius:8px !important; border-color:#e2e8f0 !important; font-size:0.9rem !important; }
div[data-baseweb="select"]>div:focus-within, div[data-baseweb="input"]>div:focus-within, textarea:focus { border-color:#3b82f6 !important; box-shadow:0 0 0 3px rgba(59,130,246,.12) !important; }
.stButton>button[kind="primary"] { background:#2563eb !important; color:#fff !important; border:none !important; border-radius:9px !important; padding:.65rem 1.5rem !important; font-size:.9rem !important; font-weight:600 !important; box-shadow:0 2px 8px rgba(37,99,235,.25); }
.stButton>button[kind="primary"]:hover { opacity:.9; transform:translateY(-1px); }
.stDownloadButton>button { border-radius:9px !important; font-size:.875rem !important; font-weight:500 !important; border-color:#e2e8f0 !important; color:#334155 !important; background:#fff !important; }
.node-card { background:#fff; border:1px solid #e2e8f0; border-left:4px solid #cbd5e1; border-radius:10px; padding:14px 18px; margin-bottom:10px; }
.node-card.active { border-left-color:#3b82f6; background:#eff6ff; }
.node-card.done   { border-left-color:#22c55e; background:#f0fdf4; }
.node-title { font-weight:600; font-size:.9rem; color:#1e293b; }
.node-sub { font-size:.8rem; color:#64748b; margin-top:4px; }
.node-ok  { font-size:.8rem; color:#16a34a; margin-top:4px; font-weight:500; }
button[data-baseweb="tab"] { font-size:.875rem !important; font-weight:600 !important; color:#64748b !important; }
button[data-baseweb="tab"][aria-selected="true"] { color:#2563eb !important; border-bottom-color:#2563eb !important; }
.result-box { background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:22px 26px; font-size:.9rem; line-height:1.8; color:#1e293b; }
hr { border:none; border-top:1px solid #e2e8f0 !important; margin:1.8rem 0 !important; }
.success-banner { background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:12px 18px; color:#15803d; font-size:.875rem; font-weight:600; margin-bottom:18px; }
.warn-box { background:#fefce8; border:1px solid #fde047; border-radius:10px; padding:12px 18px; color:#854d0e; font-size:.875rem; margin-bottom:14px; }
.section-heading { font-size:.75rem; font-weight:700; letter-spacing:.08em; color:#94a3b8; text-transform:uppercase; margin-bottom:12px; }
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

# ── Agents ────────────────────────────────────────────────────────────────────
def agent_market(field, audience):
    return genai.GenerativeModel(MODEL).generate_content(f"""
You are a friendly startup advisor. Write in very simple, everyday English — like explaining to a friend.
Industry: '{field}'. Target customers: '{audience}'.
Give exactly 3 market gaps or customer pain points.
Format each as:
### 🔍 Gap [N]: [Short title]
- **What the problem is:** One plain sentence.
- **Why it matters:** One plain sentence.
- **Opportunity:** One plain sentence about what a startup can do here.
No jargon. Keep it easy to read.
""").text

def agent_risk(field, budget, market_ctx):
    return genai.GenerativeModel(MODEL).generate_content(f"""
You are a friendly business risk advisor. Write in very simple English — no jargon.
Industry: '{field}'. Budget level: '{budget}'. Market context: {market_ctx}
Give exactly 3 risks a startup in this space might face.
Format each as:
### ⚠️ Risk [N]: [Short title]
- **What could go wrong:** One plain sentence.
- **Why this happens:** One plain sentence.
- **How to avoid it:** One plain, actionable sentence.
""").text

def agent_budget(field, budget, idea, market_ctx):
    return genai.GenerativeModel(MODEL).generate_content(f"""
You are a friendly financial advisor for startups. Write in very simple, clear English.
Industry: '{field}'. Budget level: '{budget}'. Startup idea: '{idea}'.
Market context: {market_ctx}
Budget ranges: Small=$1,000–$5,000 | Medium=$5,000–$25,000 | Large=$25,000–$100,000
Pick a specific number in the right range and use it throughout.

### 💵 Total Estimated Budget
State the total in one line, e.g. "Your estimated starting budget: **$8,000**"

### 📊 How to Spend It (Budget Breakdown)
| Category | Estimated Cost | % of Budget | What it covers |
|----------|---------------|-------------|----------------|
(5–7 rows. Amounts must add up to the total.)

### 💡 Money-Saving Tips
Exactly 3 bullet points. Practical and simple.
- 💰 **Tip:** [what to do and why it saves money]

### 🚀 When Will You Need More Money?
- **Month [N]:** [Simple sentence about when/why you'd need to raise or reinvest]
""").text

def agent_roadmap(idea, market_ctx, risk_ctx):
    return genai.GenerativeModel(MODEL).generate_content(f"""
You are a startup coach. Write in very simple English.
Startup idea: '{idea}'. Market context: {market_ctx}. Risks: {risk_ctx}

Create a Month 1 action plan broken into 4 weeks.
For EACH week:
### 📅 Week [N] — [Short week title]
| Task | Why it matters | Time needed |
|------|---------------|-------------|
| [task 1] | [simple reason] | [e.g. 2 days] |
| [task 2] | [simple reason] | [e.g. 1 day] |
| [task 3] | [simple reason] | [e.g. 3 days] |

**Goal for the week:** One sentence on what success looks like.

Keep language simple. Use action verbs. Be specific.
""").text

# ── PDF builder ───────────────────────────────────────────────────────────────
def build_pdf(field, budget, audience, idea, res1, res2, res3, res4):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm,
    )

    BLUE      = colors.HexColor("#2563eb")
    BLUE_LITE = colors.HexColor("#dbeafe")
    GREEN     = colors.HexColor("#16a34a")
    GREEN_LT  = colors.HexColor("#dcfce7")
    AMBER     = colors.HexColor("#d97706")
    AMBER_LT  = colors.HexColor("#fef3c7")
    PURPLE    = colors.HexColor("#7c3aed")
    PURPLE_LT = colors.HexColor("#ede9fe")
    GRAY_HD   = colors.HexColor("#1e293b")
    GRAY_MID  = colors.HexColor("#475569")
    GRAY_LT   = colors.HexColor("#f8fafc")
    BORDER    = colors.HexColor("#e2e8f0")

    base = getSampleStyleSheet()
    def S(name, **kw):
        return ParagraphStyle(name, parent=base['Normal'], **kw)

    sTitle  = S('sTitle',  fontSize=22, textColor=GRAY_HD, fontName='Helvetica-Bold', spaceAfter=4,  leading=28)
    sSub    = S('sSub',    fontSize=11, textColor=GRAY_MID, spaceAfter=14, leading=16)
    sMeta   = S('sMeta',   fontSize=9,  textColor=GRAY_MID, spaceAfter=2)
    sSecHdr = S('sSecHdr', fontSize=13, textColor=colors.white, fontName='Helvetica-Bold', leading=18)
    sH3     = S('sH3',     fontSize=11, textColor=GRAY_HD, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4, leading=15)
    sBody   = S('sBody',   fontSize=10, textColor=GRAY_HD, leading=16, spaceAfter=3)
    sBullet = S('sBullet', fontSize=10, textColor=GRAY_HD, leading=15, leftIndent=14, firstLineIndent=-10, spaceAfter=4)
    sLabel  = S('sLabel',  fontSize=9,  textColor=GRAY_MID, fontName='Helvetica-Bold', spaceAfter=2, spaceBefore=6)
    sTH     = S('sTH',     fontSize=9,  textColor=colors.white, fontName='Helvetica-Bold', leading=13)
    sTD     = S('sTD',     fontSize=9,  textColor=GRAY_HD, leading=13)
    sFoot   = S('sFoot',   fontSize=8,  textColor=GRAY_MID, alignment=TA_CENTER)

    story = []

    # Title block
    story.append(Paragraph("AI Business Guider", sTitle))
    story.append(Paragraph("Your complete startup blueprint — market gaps, risks, budget &amp; action plan", sSub))

    meta_tbl = Table(
        [[Paragraph(f"<b>Industry:</b> {field}", sMeta),
          Paragraph(f"<b>Budget:</b> {budget}", sMeta),
          Paragraph(f"<b>Customers:</b> {audience}", sMeta)]],
        colWidths=["33%","33%","34%"]
    )
    meta_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), GRAY_LT),
        ('BOX',        (0,0),(-1,-1), 0.5, BORDER),
        ('ROWPADDING', (0,0),(-1,-1), 7),
        ('VALIGN',     (0,0),(-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 16))

    def sec_header(title, color):
        t = Table([[Paragraph(title, sSecHdr)]], colWidths=["100%"])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,-1), color),
            ('ROWPADDING', (0,0),(-1,-1), 10),
        ]))
        return t

    def md_to_flowables(text, hdr_color):
        items = []
        lines = text.strip().split('\n')
        in_table = False
        tbl_rows = []

        def flush_table():
            nonlocal tbl_rows, in_table
            if not tbl_rows:
                return
            header = [c.strip() for c in tbl_rows[0].split('|') if c.strip()]
            body   = tbl_rows[2:]  # skip separator
            col_n  = max(len(header), 1)
            avail  = 170 * mm
            col_w  = [avail / col_n] * col_n

            data = [[Paragraph(c, sTH) for c in header]]
            for row in body:
                cells = [c.strip() for c in row.split('|') if c.strip()]
                while len(cells) < col_n: cells.append('')
                data.append([Paragraph(c[:300], sTD) for c in cells[:col_n]])

            t = Table(data, colWidths=col_w, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND',    (0,0),(-1,0),  hdr_color),
                ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, GRAY_LT]),
                ('BOX',           (0,0),(-1,-1), 0.5, BORDER),
                ('INNERGRID',     (0,0),(-1,-1), 0.3, BORDER),
                ('ROWPADDING',    (0,0),(-1,-1), 6),
                ('VALIGN',        (0,0),(-1,-1), 'TOP'),
            ]))
            items.append(t)
            items.append(Spacer(1, 8))
            tbl_rows.clear()
            in_table = False

        for line in lines:
            s = line.strip()
            if s.startswith('|'):
                in_table = True
                tbl_rows.append(s.strip('|'))
                continue
            else:
                if in_table:
                    flush_table()
            if not s:
                items.append(Spacer(1, 4)); continue

            def bold(t):
                return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)

            if s.startswith('### ') or s.startswith('## '):
                items.append(Paragraph(bold(s.lstrip('#').strip()), sH3))
            elif s.startswith('- ') or s.startswith('* '):
                items.append(Paragraph(f"• {bold(s[2:])}", sBullet))
            elif s.startswith('**') and s.endswith('**'):
                items.append(Paragraph(bold(s), sLabel))
            else:
                items.append(Paragraph(bold(s), sBody))

        if in_table:
            flush_table()
        return items

    SECTIONS = [
        ("🔍 Market Gaps & Opportunities", res1, BLUE,   BLUE_LITE),
        ("⚠️  Risks & How to Avoid Them",  res2, AMBER,  AMBER_LT),
        ("💵 Budget Breakdown",             res3, GREEN,  GREEN_LT),
        ("📅 4-Week Action Plan",           res4, PURPLE, PURPLE_LT),
    ]

    for title, content, color, lite in SECTIONS:
        story.append(sec_header(title, color))
        story.append(Spacer(1, 8))
        story.extend(md_to_flowables(content, color))
        story.append(Spacer(1, 12))
        story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER))
        story.append(Spacer(1, 10))

    story.append(Paragraph(
        f"Generated by AI Business Guider &nbsp;|&nbsp; {field} &nbsp;|&nbsp; {budget}",
        sFoot
    ))

    doc.build(story)
    return buf.getvalue()

# ── Helper ─────────────────────────────────────────────────────────────────────
def node_html(icon, title, sub, state="idle"):
    cls  = {"idle":"","active":"active","done":"done"}.get(state,"")
    scls = "node-ok" if state=="done" else "node-sub"
    tick = "✓ " if state=="done" else ("⏳ " if state=="active" else "")
    return (
        f'<div class="node-card {cls}">'
        f'<div class="node-title">{icon} {title}</div>'
        f'<div class="{scls}">{tick}{sub}</div>'
        f'</div>'
    )

# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("## 💼 AI Business Guider")
st.markdown(
    "<p style='color:#64748b;font-size:.9rem;margin-top:-8px;margin-bottom:20px;'>"
    "Get a simple, deep guide — market gaps, risks, budget breakdown, and a week-by-week action plan."
    "</p>", unsafe_allow_html=True
)

st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">Your startup details</div>', unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a:
    field    = st.selectbox("Industry", ["Technology & Software","Healthcare & Medical Technology","Education Technology","E-Commerce","FoodTech & Hospitality"])
    budget   = st.selectbox("Starting budget", ["Small Budget","Medium Budget","Large Budget"])
with col_b:
    audience = st.text_input("Who are your customers?", placeholder="e.g., college students, busy parents…")
    idea     = st.text_area("What is your startup idea?", height=110, placeholder="e.g., AI-driven gamified math learning…")
st.markdown("<br>", unsafe_allow_html=True)
run = st.button("🚀  Generate Full Business Guide", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── Pipeline ───────────────────────────────────────────────────────────────────
if run:
    if not audience.strip() or not idea.strip():
        st.markdown('<div class="warn-box">⚠️ Please fill in both <b>customers</b> and <b>startup idea</b>.</div>', unsafe_allow_html=True)
        st.stop()

    st.markdown("---")
    st.markdown('<div class="section-heading">Live processing — 4 AI agents</div>', unsafe_allow_html=True)
    ph1, ph2, ph3, ph4 = st.empty(), st.empty(), st.empty(), st.empty()

    def run_agent(ph_active, label, icon, msg_active, msg_done, fn, *args):
        ph_active.markdown(node_html(icon, label, msg_active, "active"), unsafe_allow_html=True)
        try:
            result = fn(*args)
        except Exception as e:
            st.error(f"{label} error: {e}"); st.stop()
        ph_active.markdown(node_html(icon, label, msg_done, "done"), unsafe_allow_html=True)
        return result

    ph2.markdown(node_html("⚠️", "Risk advisor",   "Waiting…"), unsafe_allow_html=True)
    ph3.markdown(node_html("💵", "Budget planner", "Waiting…"), unsafe_allow_html=True)
    ph4.markdown(node_html("📋", "Roadmap coach",  "Waiting…"), unsafe_allow_html=True)

    res1 = run_agent(ph1, "Market analyst", "🔍", "Finding market gaps…",            "Market gaps mapped.",   agent_market,  field, audience)
    res2 = run_agent(ph2, "Risk advisor",   "⚠️", "Finding risks to watch out for…", "Risks identified.",     agent_risk,    field, budget, res1)
    res3 = run_agent(ph3, "Budget planner", "💵", "Building budget breakdown…",       "Budget plan ready.",    agent_budget,  field, budget, idea, res1)
    res4 = run_agent(ph4, "Roadmap coach",  "📋", "Building week-by-week plan…",      "Action plan compiled.", agent_roadmap, idea, res1, res2)

    st.markdown("---")
    st.markdown('<div class="success-banner">✨ Your full business guide is ready!</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Market gaps","⚠️ Risks","💵 Budget","📅 4-week plan"])
    for tab, res in zip([tab1,tab2,tab3,tab4],[res1,res2,res3,res4]):
        with tab:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(res)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner("Building your PDF…"):
        pdf_bytes = build_pdf(field, budget, audience, idea, res1, res2, res3, res4)

    st.download_button(
        label="📥  Download Business Guide as PDF",
        data=pdf_bytes,
        file_name="business_guide.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
