# 💼 AI Business Guider

A simple Streamlit app that uses 4 connected AI agents to turn a startup idea into a complete, ready-to-use business blueprint. Instead of generic AI answers, it builds a tailored strategy you can read on-screen or download as a clean PDF.

---

## 🚀 Key Features

* **Clean Interface:** A modern, interactive SaaS-style layout built with custom CSS cards and hover effects.
* **4-Agent AI Pipeline:**
  * 🔍 **Market Analyst:** Finds hidden customer pain points and market gaps.
  * ⚠️ **Risk Advisor:** Flags major pitfalls and provides realistic fixes.
  * 💵 **Budget Planner:** Calculates exact costs and creates a clear expense table.
  * 📋 **Roadmap Coach:** Builds a direct, step-by-step 4-week execution plan.
* **PDF Downloads:** Converts the AI's markdown output into a clean, professional PDF file using ReportLab.

---

## 🛠️ Quick Setup Guide

### 1. Clone the Repository
```bash
git clone [https://github.com/MOLLYSAXENA/ai-business-guider.git](https://github.com/MOLLYSAXENA/ai-business-guider.git)
cd ai-business-guider

```
### 2. Install the Necessary Packages

Make sure you have your virtual environment active, then run:
```bash
pip install streamlit google-generativeai reportlab
```
### 3. Add Your Gemini API Key
Create the Streamlit secrets folder and file:
```bash
mkdir .streamlit
touch .streamlit/secrets.toml
Open .streamlit/secrets.toml and

add your Google AI Studio key:

Ini, TOML
GEMINI_API_KEY = "your-actual-api-key-here"

```
### 4. Run the Application
  ```bash
streamlit run app.py
```
