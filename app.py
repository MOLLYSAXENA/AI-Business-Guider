import streamlit as st
import google.generativeai as genai

# 1. Premium Cyberpunk/Corporate Page Setup
st.set_page_config(page_title="IncuBot Matrix | Multi-Agent Network", page_icon="⚡", layout="wide")

# Custom Injecting Enterprise Theme & Layout Rules
st.markdown("""
    <style>
    body { background-color: #0b0f19; }
    .stApp { background-color: #0b0f19; }
    .agent-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .agent-active { border-left-color: #10b981; }
    .metric-value {
        font-family: 'Courier New', monospace;
        font-size: 24px;
        font-weight: bold;
        color: #10b981;
    }
    </style>
""", unsafe_allow_html=True)

# Secure Key Initialization
api_key = st.secrets.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("🚨 Configuration Error: GEMINI_API_KEY is missing in Streamlit Secrets.")

# --- MULTI-AGENT COMPONENT CORE LOGIC ---
def run_agent_1(sector, audience):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Act as an NLP Market Intelligence Agent. Analyze raw customer complaints and trends for '{sector}' targeting '{audience}'. Give a structured report with clear sections on Market Gaps, Psychological Triggers, and Language Metaphors used by customers. Use rich formatting and bullets."
    return model.generate_content(prompt).text

def run_agent_2(sector, runway, context_1):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Act as a Venture Capital Risk Auditor. Read this NLP market analysis: '{context_1}'. For a company entering the '{sector}' space with a '{runway}' runway, detail exactly 3 massive tactical failures or regulatory traps they will hit. Be brutal, highly technical, and precise."
    return model.generate_content(prompt).text

def run_agent_3(idea, context_1, context_2):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Act as the Chief Architect Node. Combine the Market Gaps: '{context_1}' and Risk Vector Logs: '{context_2}' to design an engineering and launch roadmap for this core vision: '{idea}'. Output a detailed week-by-week sprint for Month 1."
    return model.generate_content(prompt).text

# --- SYSTEM UI LAYOUT ---
st.title("⚡ IncuBot Matrix: Autonomous Multi-Agent Node")
st.markdown("##### System Architecture: **Sequential Token-Passing Orchestration Matrix** | Core Node: Molly Saxena (CSE-AIML)")
st.markdown("---")

# Metrics Overview Strip
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("<div class='agent-card'><p style='color:#94a3b8; margin:0;'>NETWORK STATUS</p><p class='metric-value'>ONLINE // SECURE</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='agent-card'><p style='color:#94a3b8; margin:0;'>TOTAL DEPLOYED NODES</p><p class='metric-value'>3 Active Agents</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='agent-card'><p style='color:#94a3b8; margin:0;'>PIPELINE STRUCTURE</p><p class='metric-value'>Sequential Chain</p></div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div class='agent-card'><p style='color:#94a3b8; margin:0;'>CORE ENGINE LAYER</p><p class='metric-value'>Gemini Flash Node</p></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_input, col_output = st.columns([1, 1.3])

with col_input:
    st.subheader("🛠️ Environmental Directives")
    
    sector = st.selectbox("Ecosystem Domain", ["DeFi / FinTech Layer", "B2B SaaS / Enterprise Infrastructure", "EdTech / Adaptive Learning Systems", "HealthTech / BioInformatics", "DeepTech / Autonomous Agents"])
    runway = st.selectbox("Capital Deployment Vector", ["Lean Bootstrap Pipeline (Low Buffer)", "Angel / Seed Stage Injection (Mid Buffer)", "Venture Scale Capital (Aggressive Burn)"])
    audience = st.text_input("Target Audience Parameters", placeholder="e.g., Independent doctors, tier-2 retail merchants...")
    
    st.markdown("---")
    st.subheader("💡 Founder Core Architecture Blueprint")
    idea = st.text_area("Input business vision / technical roadmap framework:", height=220, placeholder="Describe your product core mechanics, tech stack, and target value loop...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    deploy_btn = st.button("🚀 TRIGGER AGENT NETWORK EXECUTIONS", type="primary", use_container_width=True)

with col_output:
    st.subheader("🖥️ Agent Matrix Operations Log")
    
    if deploy_btn:
        if idea.strip() != "" and audience.strip() != "":
            
            # --- AGENT 1 PROCESS LOOP ---
            a1_status = st.markdown("<div class='agent-card agent-active'>⚙️ <strong>Deploying Agent 1:</strong> Mining unstructured market text grids and sentiment matrix arrays...</div>", unsafe_allow_html=True)
            a1_res = run_agent_1(sector, audience)
            a1_status.markdown("<div class='agent-card'>✅ <strong>Agent 1 Operations Complete:</strong> Semantic intelligence matrix extracted successfully.</div>", unsafe_allow_html=True)
            
            # --- AGENT 2 PROCESS LOOP ---
            a2_status = st.markdown("<div class='agent-card agent-active'>⚙️ <strong>Deploying Agent 2:</strong> Passing Agent 1 context arrays downstream to execute brutal risk vector audits...</div>", unsafe_allow_html=True)
            a2_res = run_agent_2(sector, runway, a1_res)
            a2_status.markdown("<div class='agent-card'>✅ <strong>Agent 2 Operations Complete:</strong> 3 Structural risk layers identified and flagged.</div>", unsafe_allow_html=True)
            
            # --- AGENT 3 PROCESS LOOP ---
            a3_status = st.markdown("<div class='agent-card agent-active'>⚙️ <strong>Deploying Agent 3:</strong> Orchestrating final synthesis engine to map the launch blueprint...</div>", unsafe_allow_html=True)
            a3_res = run_agent_3(idea, a1_res, a2_res)
            a3_status.markdown("<div class='agent-card'>✅ <strong>Agent 3 Operations Complete:</strong> Final corporate strategy compiled.</div>", unsafe_allow_html=True)
            
            st.success("🎉 Multi-Agent Core Synchronized Successfully!")
            st.markdown("### 📊 Consolidated Strategy Console Layout")
            
            # Beautiful Tabbed Panel for Output Sorting
            tab1, tab2, tab3 = st.tabs(["🔍 Market Intelligence (Agent 1)", "🚨 Risk Assessment (Agent 2)", "📅 4-Week Blueprint (Agent 3)"])
            
            with tab1:
                st.markdown(a1_res)
            with tab2:
                st.markdown(a2_res)
            with tab3:
                st.markdown(a3_res)
                
            # Formatting full text data for download asset feature
            full_report_text = f"=== INCUBOT AI STRATEGY REPORT ===\n\n[PART 1: NLP MARKET RESEARCH]\n{a1_res}\n\n[PART 2: RISK AUDIT]\n{a2_res}\n\n[PART 3: EXECUTION SPRINT]\n{a3_res}"
            
            st.markdown("---")
            st.download_button(
                label="📥 Download Full Consolidated Operational Strategy Blueprint",
                data=full_report_text,
                file_name="incubot_strategy_blueprint.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        else:
            st.warning("Execution Halted: Ensure both Target Audience Parameters and Core Architecture fields are populated.")
