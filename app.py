import streamlit as st
import google.generativeai as genai

# 1. Premium Page Configuration
st.set_page_config(page_title="IncuBot Pro | Multi-Agent Hub", page_icon="🤖", layout="wide")

# Dark Aesthetic Styling
st.markdown("""
    <style>
    .agent-box {
        background-color: #0f172a;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #1e293b;
        margin-bottom: 15px;
    }
    .console-text {
        font-family: 'Courier New', Courier, monospace;
        color: #10b981;
    }
    </style>
""", unsafe_allow_html=True)

# API Gate
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "GEMINI_KEY"

genai.configure(api_key=api_key)

# =====================================================================
# 🧠 DEFINING THE 3 GENUINE SEPARATE AI AGENTS
# =====================================================================

def run_nlp_researcher_agent(sector, audience):
    """AGENT 1: Independent NLP Text Miner specializing in User Sentiment"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    system_persona = """
    You are a specialized NLP Market Analyst. Your ONLY job is to analyze text patterns, 
    social media rants, and forums to extract customer pain points and semantic complaints 
    about an industry sector. Do not give financial advice. Give a bulleted sentiment report.
    """
    prompt = f"Analyze the customer sentiment data and language patterns for the '{sector}' sector targeting '{audience}'."
    
    response = model.generate_content([system_persona, prompt])
    return response.text

def run_financial_auditor_agent(sector, runway, nlp_research_context):
    """AGENT 2: Independent Risk Compliance Officer analyzing Agent 1's report"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    system_persona = """
    You are a brutal Venture Capital Risk Auditor. Your ONLY job is to find 2 fatal financial 
    flaws or legal traps in a business concept. You must look at the market sentiment data 
    provided by Agent 1 to check if the budget matches the customer pain points.
    """
    prompt = f"""
    Review this industry: {sector} with a budget tier of: {runway}.
    Cross-reference it with the Customer Sentiment report provided by Agent 1 below, 
    and output exactly 2 severe risk vectors.
    
    [Agent 1 Context]:
    {nlp_research_context}
    """
    
    response = model.generate_content([system_persona, prompt])
    return response.text

def run_genai_orchestrator_agent(idea, nlp_context, risk_context):
    """AGENT 3: The Project Manager. Merges all contexts into a final blueprint"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    system_persona = """
    You are a Senior Technical Project Manager and Startup Architect. Your job is to take the 
    raw customer insights from Agent 1 and the critical risks from Agent 2, combine them with 
    the founder's core vision, and build a 4-week execution blueprint.
    """
    prompt = f"""
    Synthesize a complete business plan for this startup idea: '{idea}'.
    You must directly address the market gaps found by Agent 1 and mitigate the financial traps flagged by Agent 2.
    
    [Agent 1 Sentiment Input]:
    {nlp_context}
    
    [Agent 2 Risk Input]:
    {risk_context}
    """
    
    response = model.generate_content([system_persona, prompt])
    return response.text

# =====================================================================
# 🖥️ STREAMLIT INTERFACE
# =====================================================================

st.title("🤖 IncuBot Pro: Genuine Multi-Agent Network")
st.markdown("##### Enterprise Design: **Orchestrated Multi-Agent Sequential Chain (NLP ➡️ Risk ➡️ GenAI Execution)**")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Network Configurations")
    sector = st.selectbox("Ecosystem", ["DeFi / FinTech", "B2B SaaS / Enterprise", "EdTech / EdSystems", "HealthTech / BioTech"])
    runway = st.selectbox("Capital Scale", ["Lean Bootstrap", "Angel Stage Funding", "Venture Scale High-Burn"])
    audience = st.text_input("Target Audience", placeholder="e.g., Doctors, College Students...")
    st.markdown("---")
    deploy_network = st.button("Deploy Multi-Agent Chain", type="primary", use_container_width=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("💡 The Founder's Vision")
    idea = st.text_area("Paste the business concept architecture:", height=300, placeholder="Describe the product mechanics and core concept...")

with col2:
    st.subheader("🖥️ Multi-Agent Live Logs & Orchestration")
    
    if deploy_network:
        if idea.strip() != "" and audience.strip() != "":
            
            # --- STEP 1: DEPLOY AGENT 1 ---
            log_box_1 = st.empty()
            with log_box_1.container():
                st.markdown("<div class='agent-box'><span class='console-text'>🔄 Initializing Agent 1: NLP Market Researcher...</span></div>", unsafe_allow_html=True)
            
            agent1_output = run_nlp_researcher_agent(sector, audience)
            
            with log_box_1.container():
                st.markdown("<div class='agent-box'><strong>🟢 Agent 1 (NLP Sentiment Analyst) Complete</strong></div>", unsafe_allow_html=True)
                with st.expander("View Agent 1 Raw Output Token Data"):
                    st.write(agent1_output)
            
            # --- STEP 2: DEPLOY AGENT 2 ---
            log_box_2 = st.empty()
            with log_box_2.container():
                st.markdown("<div class='agent-box'><span class='console-text'>🔄 Initializing Agent 2: Strategic Risk Auditor... (Injecting Agent 1 Context)</span></div>", unsafe_allow_html=True)
            
            agent2_output = run_financial_auditor_agent(sector, runway, agent1_output)
            
            with log_box_2.container():
                st.markdown("<div class='agent-box'><strong>🟢 Agent 2 (Risk Auditor) Complete</strong></div>", unsafe_allow_html=True)
                with st.expander("View Agent 2 Risk Vector Flags"):
                    st.write(agent2_output)
                    
            # --- STEP 3: DEPLOY AGENT 3 ---
            log_box_3 = st.empty()
            with log_box_3.container():
                st.markdown("<div class='agent-box'><span class='console-text'>🔄 Initializing Agent 3: GenAI Executive Architect... (Compiling Matrix)</span></div>", unsafe_allow_html=True)
            
            final_report = run_genai_orchestrator_agent(idea, agent1_output, agent2_output)
            
            with log_box_3.container():
                st.markdown("<div class='agent-box'><strong>🟢 Agent 3 (Orchestrator) Generation Complete</strong></div>", unsafe_allow_html=True)
            
            # Final Combined Report Output
            st.success("🎉 Full Multi-Agent Pipeline Executed Successfully!")
            st.markdown("---")
            st.markdown("## 📋 Final Consolidated Strategic Blueprint")
            st.markdown(final_report)
            
        else:
            st.warning("Please supply both Vision and Target Audience variables to trigger execution.")