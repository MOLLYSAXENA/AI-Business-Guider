import streamlit as st
import google.generativeai as genai

# 1. Page Configuration - Clean & Professional Layout
st.set_page_config(page_title="IncuBot AI | Multi-Agent Network", page_icon="🚀", layout="wide")

# Modern Minimalist Enterprise Styling
st.markdown("""
    <style>
    .step-box {
        background-color: #f8fafc;
        border-left: 5px solid #2563eb;
        border-top: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .check-text {
        color: #16a34a;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Secure API Key Setup from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Configuration Error: GEMINI_API_KEY missing in Streamlit Secrets.")

# =====================================================================
# 🧠 BACKEND ENGINE: PURE ENGLISH PROMPTS FOR BEST LLM REASONING
# =====================================================================

def agent_1_market_analysis(field, target_audience):
    """Agent 1: Continuous NLP Text Processing to Extract Gaps"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    english_prompt = f"""
    You are an expert market intelligence AI agent specializing in Natural Language Processing (NLP) sentiment extraction.
    The user is launching a startup in the '{field}' sector, targeting the audience group: '{target_audience}'.
    
    Task: Extract and outline the core consumer pain points, underserved market gaps, and unmet desires based on customer behavioral patterns.
    
    Output Formatting Rule: Write the response in highly readable, professional business language using clear bullet points. Break it down into logical subsections.
    """
    return model.generate_content(english_prompt).text

def agent_2_risk_audit(field, budget_tier, market_context):
    """Agent 2: Venture Risk & Capital Runway Auditor"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    english_prompt = f"""
    You are a strict financial risk consultant and venture capital auditor.
    The business is operating in the '{field}' industry under a '{budget_tier}' financial runway constraint.
    
    Task: Review the market intelligence context provided by Agent 1 below:
    [Context]: {market_context}
    
    Isolate and explicitly state exactly 3 critical operational risks, legal bottlenecks, or financial pitfalls that could cause early-stage bankruptcy for this startup idea under this specific budget constraint.
    
    Output Formatting Rule: Write in clean, concise, point-by-point format. Keep the tone highly analytical and cautionary.
    """
    return model.generate_content(english_prompt).text

def agent_3_roadmap_orchestrator(idea, market_context, risk_context):
    """Agent 3: Strategic Blueprint Generator"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    english_prompt = f"""
    You are a premier startup incubation director and growth architect.
    The founder's core vision is: '{idea}'.
    
    Task: Synthesize the customer gaps from Agent 1 and the risk mitigations from Agent 2 to build a structured, step-by-step tactical launch playbook.
    [Agent 1 Context]: {market_context}
    [Agent 2 Context]: {risk_context}
    
    Generate a detailed week-by-week roadmap for Month 1 (Week 1 through Week 4) detailing concrete execution steps the founder must take.
    
    Output Formatting Rule: Use clean markdown headers for each week. Keep the language direct, actionable, and objective.
    """
    return model.generate_content(english_prompt).text

# =====================================================================
# 🖥️ CLEAN & PROFESSIONAL ENTERPRISE INTERFACE
# =====================================================================

st.title("🚀 IncuBot AI: Multi-Agent Incubation Network")
st.markdown("An automated pipeline orchestrating specialized AI nodes for comprehensive market analysis, risk mitigation, and launch execution planning.")
st.markdown("---")

col_inputs, col_results = st.columns([1, 1.2])

with col_inputs:
    st.markdown("### 📝 Strategic Input Directives")
    
    # Fixed Missing Commas and Cleaned Up List Formatting
    field = st.selectbox(
        "Industry Ecosystem / Vertical", 
        [
            "Technology & Software", 
            "Healthcare & Medical Technology", 
            "Education Technology", 
            "E-Commerce", 
            "FoodTech & Hospitality"
        ]
    )
    
    # Capital/Budget Runway Selection
    budget_tier = st.selectbox(
        "What is your starting budget?", 
        [
            "Small Budget", 
            "Medium Budget", 
            "Large Budget"
        ]
    )
    
    # Clean User Text Inputs
    target_audience = st.text_input(
        "Who are your real customers?", 
        placeholder="e.g., college students, housewives, startups..."
    )
    
    idea = st.text_area(
        "Startup Core Concept & Architecture Description", 
        height=150, 
        placeholder="e.g., An AI-driven gamified math learning platform that utilizes adaptive micro-lessons to help primary school students learn complex concepts through interactive puzzle mechanics..."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.button("🚀 EXECUTE MULTI-AGENT ANALYSIS", type="primary", use_container_width=True)

with col_results:
    st.markdown("### 🖥️ Real-Time Node Orchestration Matrix")
    
    if submit_btn:
        if idea.strip() != "" and target_audience.strip() != "":
            
            # --- AGENT 1 EXECUTION ---
            with st.container():
                st.markdown("<div class='step-box'>🕵️‍♂️ <strong>Agent 1 (Market Analyst):</strong> Extracting customer behavioral insights and market gap arrays...</div>", unsafe_allow_html=True)
                res_1 = agent_1_market_analysis(field, target_audience)
                st.markdown("<span class='check-text'>✓ Agent 1 processing complete. Semantic data transferred downstream.</span>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- AGENT 2 EXECUTION ---
            with st.container():
                st.markdown("<div class='step-box'>💰 <strong>Agent 2 (Risk Auditor):</strong> Assessing financial vulnerabilities and compliance constraints...</div>", unsafe_allow_html=True)
                res_2 = agent_2_risk_audit(field, budget_tier, res_1)
                st.markdown("<span class='check-text'>✓ Agent 2 processing complete. Structural risks flagged and mapped.</span>", unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- AGENT 3 EXECUTION ---
            with st.container():
                st.markdown("<div class='step-box'>📋 <strong>Agent 3 (Startup Coach):</strong> Synthesizing inputs to generate operational launch playbook...</div>", unsafe_allow_html=True)
                res_3 = agent_3_roadmap_orchestrator(idea, res_1, res_2)
                st.markdown("<span class='check-text'>✓ Agent 3 processing complete. Final compilation synchronized.</span>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.success("✨ Strategic Blueprint Compiled Successfully!")
            
            # Clean Corporate Sorted Output Tabs
            tab1, tab2, tab3 = st.tabs(["🔍 Market Gaps & Insights", "🚨 Risk & Runway Audit", "📅 4-Week Launch Roadmap"])
            
            with tab1:
                st.markdown(res_1)
            with tab2:
                st.markdown(res_2)
            with tab3:
                st.markdown(res_3)
                
            # Professional Download Structure
            full_report = f"=== INCUBOT AI STRATEGIC REPORT ===\n\n[SECTION 1: MARKET & CUSTOMER RESEARCH]\n{res_1}\n\n[SECTION 2: BUDGET & STRUCTURAL RISKS]\n{res_2}\n\n[SECTION 3: 4-WEEK ACTION MATRIX]\n{res_3}"
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Complete Operational Strategy Document",
                data=full_report,
                file_name="strategic_startup_blueprint.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        else:
            st.warning("Validation Error: Please populate both the 'Who are your real customers?' and 'Startup Core Concept' fields before executing the network pipeline.")
