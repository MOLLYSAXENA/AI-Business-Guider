import streamlit as st
import google.generativeai as genai

# 1. Page Config
st.set_page_config(page_title="IncuBot Pro | Multi-Agent Hub", page_icon="🤖", layout="wide")

# Styling
st.markdown("""
    <style>
    .agent-box { background-color: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; margin-bottom: 15px; }
    .console-text { font-family: 'Courier New', Courier, monospace; color: #10b981; }
    </style>
""", unsafe_allow_html=True)

# --- SECURE KEY EXTRACTION ---
# Yeh line tumhari special enterprise key ko properly fetch karegi
api_key = st.secrets.get("GEMINI_API_KEY", "YOUR_LOCAL_GEMINI_API_KEY")

# Hard authentication mapping for enterprise keys
if api_key and api_key != "YOUR_LOCAL_GEMINI_API_KEY":
    genai.configure(api_key=api_key)
else:
    st.error("API Key missing in Streamlit Secrets!")

# --- MULTI-AGENT FUNCTIONS ---
def run_nlp_researcher_agent(sector, audience):
    model = genai.GenerativeModel('gemini-1.5-flash')
    system = "You are a specialized NLP Market Analyst. Extract customer pain points in bullets."
    response = model.generate_content(f"{system}\n\nAnalyze '{sector}' for '{audience}'.")
    return response.text

def run_financial_auditor_agent(sector, runway, nlp_context):
    model = genai.GenerativeModel('gemini-1.5-flash')
    system = "You are a brutal Venture Capital Risk Auditor. Output exactly 2 severe financial/operational risks."
    response = model.generate_content(f"{system}\n\nSector: {sector}, Runway: {runway}.\nContext: {nlp_context}")
    return response.text

def run_genai_orchestrator_agent(idea, nlp_context, risk_context):
    model = genai.GenerativeModel('gemini-1.5-flash')
    system = "You are a Senior Startup Architect. Create a structured 4-week roadmap using the provided contexts."
    response = model.generate_content(f"{system}\n\nIdea: {idea}\nNLP: {nlp_context}\nRisks: {risk_context}")
    return response.text

# --- UI INTERFACE ---
st.title("🤖 IncuBot Pro: Genuine Multi-Agent Network")
st.markdown("##### Enterprise Design: **Orchestrated Multi-Agent Sequential Chain**")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Network Configurations")
    sector = st.selectbox("Ecosystem", ["DeFi / FinTech", "B2B SaaS / Enterprise", "EdTech / EdSystems", "HealthTech / BioTech"])
    runway = st.selectbox("Capital Scale", ["Lean Bootstrap", "Angel Stage Funding", "Venture Scale High-Burn"])
    audience = st.text_input("Target Audience", placeholder="e.g., Doctors, College Students...")
    deploy_network = st.button("Deploy Multi-Agent Chain", type="primary", use_container_width=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("💡 The Founder's Vision")
    idea = st.text_area("Paste the business concept:", height=300, placeholder="Describe the product mechanics...")

with col2:
    st.subheader("🖥️ Multi-Agent Live Logs")
    
    if deploy_network:
        if idea.strip() != "" and audience.strip() != "":
            
            # Agent 1
            st.markdown("<div class='agent-box'><span class='console-text'>🔄 Agent 1 Running...</span></div>", unsafe_allow_html=True)
            a1_out = run_nlp_researcher_agent(sector, audience)
            st.markdown("<div class='agent-box'><strong>🟢 Agent 1 Complete</strong></div>", unsafe_allow_html=True)
            
            # Agent 2
            st.markdown("<div class='agent-box'><span class='console-text'>🔄 Agent 2 Running...</span></div>", unsafe_allow_html=True)
            a2_out = run_financial_auditor_agent(sector, runway, a1_out)
            st.markdown("<div class='agent-box'><strong>🟢 Agent 2 Complete</strong></div>", unsafe_allow_html=True)
            
            # Agent 3
            st.markdown("<div class='agent-box'><span class='console-text'>🔄 Agent 3 Running...</span></div>", unsafe_allow_html=True)
            final_report = run_genai_orchestrator_agent(idea, a1_out, a2_out)
            st.markdown("<div class='agent-box'><strong>🟢 Agent 3 Complete</strong></div>", unsafe_allow_html=True)
            
            st.success("🎉 Multi-Agent Pipeline Executed Successfully!")
            st.markdown("---")
            st.markdown(final_report)
