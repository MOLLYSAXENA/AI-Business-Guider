import streamlit as st
import google.generativeai as genai

# 1. Page Configuration - Modern Enterprise Layout
st.set_page_config(page_title="AI Business Guider", page_icon="💼", layout="wide")

# Custom Modern CSS with Flexbox, Cards, and Hover Effects
st.markdown("""
    <style>
    /* Global Base Tweaks */
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    
    /* Input Container Card */
    .input-card {
        background: FFFCEB;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 25px;
    }
    
    /* Flexbox Pipeline Matrix */
    .pipeline-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 20px;
    }
    
    /* Live Status Nodes / Cards */
    .node-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 6px solid #2563eb;
        padding: 16px 20px;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Interactive Hover Effect */
    .node-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.1), 0 4px 6px -2px rgba(37, 99, 235, 0.05);
        border-color: #cbd5e1;
        border-left-color: #1d4ed8;
    }
    
    .node-title {
        font-weight: 600;
        color: #1e293b;
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .node-success-text {
        color: #16a34a;
        font-size: 0.875rem;
        font-weight: 500;
        margin-top: 4px;
        display: block;
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
# 🧠 BACKEND ENGINE: OPTIMIZED FOR CONCISE, HIGH-IMPACT ANSWERS
# =====================================================================

MODEL_NAME = "gemini-2.5-flash" 

def agent_1_market_analysis(field, target_audience):
    """Agent 1: High-Density Bullet Points for Market Gaps"""
    model = genai.GenerativeModel(MODEL_NAME)
    
    english_prompt = f"""
    You are a startup market analyst. The user is starting a business in '{field}' targeting '{target_audience}'.
    
    Task: Identify core consumer pain points and underserved gaps.
    
    Formatting Rule: Be incredibly brief. Provide exactly 3 high-impact bullet points. No conversational filler or introductory fluff. Get straight to the metrics and insights.
    """
    return model.generate_content(english_prompt).text

def agent_2_risk_audit(field, budget_tier, market_context):
    """Agent 2: Punchy Venture Capital Risk Review"""
    model = genai.GenerativeModel(MODEL_NAME)
    
    english_prompt = f"""
    You are a venture capital risk auditor. The industry vertical is '{field}' with a '{budget_tier}' runway limitation.
    
    Task: Evaluate the market context: {market_context}
    
    Formatting Rule: State exactly 3 critical risks or financial traps that lead to early failure. Keep each point to a maximum of 2 sentences. No intro/outro text.
    """
    return model.generate_content(english_prompt).text

def agent_3_roadmap_orchestrator(idea, market_context, risk_context):
    """Agent 3: Sharp, Actionable Operational Milestones"""
    model = genai.GenerativeModel(MODEL_NAME)
    
    english_prompt = f"""
    You are an incubator director accelerating this core concept: '{idea}'.
    Context: {market_context} | Risks: {risk_context}
    
    Task: Create a Month 1 execution playbook broken down week by week (Weeks 1-4).
    
    Formatting Rule: Provide exactly 1 structural, clear action item for each week. Do not exceed 15 words per week. Use clean Markdown headers.
    """
    return model.generate_content(english_prompt).text

# =====================================================================
# 🖥️ INTERACTIVE INTERFACE (REORDERED LAYOUT)
# =====================================================================

st.title("💼 AI Business Guider")
st.markdown("Instantly map market opportunities, de-risk your finances, and compile a tactical launch blueprint through coordinated AI nodes.")
st.markdown("---")

# Wrap the inputs inside a scannable single block container
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown("### 📝 Enter the Details of Your Startup")

col_left, col_right = st.columns(2)

with col_left:
    field = st.selectbox(
        "Industry Ecosystem / Vertical", 
        ["Technology & Software", "Healthcare & Medical Technology", "Education Technology", "E-Commerce", "FoodTech & Hospitality"]
    )
    budget_tier = st.selectbox(
        "What is your starting budget?", 
        ["Small Budget", "Medium Budget", "Large Budget"]
    )
    target_audience = st.text_input(
        "Who are your real customers?", 
        placeholder="e.g., college students, busy parents, SaaS teams..."
    )

with col_right:
    idea = st.text_area(
        "Startup Core Concept & Architecture Description", 
        height=125, 
        placeholder="e.g., An AI-driven gamified math learning platform using adaptive micro-lessons for primary school students..."
    )

st.markdown("<br>", unsafe_allow_html=True)
submit_btn = st.button("🚀 GENERATE STRATEGIC BLUEPRINT", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Processing and Results Display Below Inputs
if submit_btn:
    if idea.strip() != "" and target_audience.strip() != "":
        st.markdown("### ⚙️ Live Strategy Processing Hub")
        
        try:
            # --- AGENT 1 EXECUTION ---
            st.markdown("""
                <div class="pipeline-container">
                    <div class="node-card">
                        <div class="node-title">🕵️‍♂️ Node 1: Market Intelligence Analyst</div>
                        <div>Extracting consumer behavioral data dynamics and finding market gap matrices...</div>
            """, unsafe_allow_html=True)
            res_1 = agent_1_market_analysis(field, target_audience)
            st.markdown(f"<span class='node-success-text'>✓ Step complete. Core market gaps successfully mapped.</span></div>", unsafe_allow_html=True)
            
            # --- AGENT 2 EXECUTION ---
            st.markdown("""
                    <div class="node-card">
                        <div class="node-title">💰 Node 2: Capital & Venture Risk Auditor</div>
                        <div>Auditing legal vulnerabilities, compliance challenges, and budget pitfalls...</div>
            """, unsafe_allow_html=True)
            res_2 = agent_2_risk_audit(field, budget_tier, res_1)
            st.markdown(f"<span class='node-success-text'>✓ Step complete. Critical failure vector arrays locked in.</span></div>", unsafe_allow_html=True)
            
            # --- AGENT 3 EXECUTION ---
            st.markdown("""
                    <div class="node-card">
                        <div class="node-title">📋 Node 3: Incubation Roadmap Director</div>
                        <div>Synthesizing strategic parameters into a lightweight growth action playbook...</div>
            """, unsafe_allow_html=True)
            res_3 = agent_3_roadmap_orchestrator(idea, res_1, res_2)
            st.markdown(f"<span class='node-success-text'>✓ Step complete. Final tactical blueprint generation synced.</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.success("✨ Strategic Blueprint Compiled Successfully!")
            
            # Clean Tab Layout for Content Delivery
            tab1, tab2, tab3 = st.tabs(["🔍 Target Gaps & Insights", "🚨 Risk & Runway Audit", "📅 4-Week Action Roadmap"])
            
            with tab1:
                st.markdown(res_1)
            with tab2:
                st.markdown(res_2)
            with tab3:
                st.markdown(res_3)
                
            # Compile Document Download Utility
            full_report = f"=== AI BUSINESS GUIDER REPORT ===\n\n[MARKET & CUSTOMER RESEARCH]\n{res_1}\n\n[BUDGET & STRUCTURAL RISKS]\n{res_2}\n\n[4-WEEK ACTION MATRIX]\n{res_3}"
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Clean Business Strategy Document",
                data=full_report,
                file_name="ai_business_guidance_blueprint.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        except Exception as e:
            st.error(f"API Engine Error: {e}")
            st.info("💡 Quick Fix: If this is an installation 404 issue, try updating the library package via terminal: `pip install --upgrade google-generativeai`")
            
    else:
        st.warning("Validation Error: Please fill out both the Target Customer and Startup Core Concept fields before running the AI processing nodes.")
