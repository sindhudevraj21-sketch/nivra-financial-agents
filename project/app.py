import streamlit as st
import sys, os
# Add project root to path for local imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.main_agent import run_agent
from typing import List, Dict, Any

def display_scenario(scenario_name, user_id, sms, manual, ocr):
    st.subheader(f"Scenario: {scenario_name} (User: {user_id})")

    # Run Agent
    result = run_agent(sms, user_id, manual, ocr)

    # Display Plan
    st.markdown("---")
    st.markdown(f"*Final Priority:* *{result['plan']['priority_level']}* | *Spend Limit:* *${result['plan']['today_spend_limit_cents'] / 100:.2f}*")
    st.markdown(f"*Micro-Task:* {result['plan']['micro_task']}")

    # Display Coach Advice
    st.subheader("🎓 Coach/Concierge Advice")
    st.markdown(f"*Investment Tip:* {result['coach_advice']['investment_tip']}")
    st.markdown(f"*Optimization:* {result['coach_advice']['optimization_suggestion']}")
    st.markdown(f"*Nudge:* {result['coach_advice']['motivational_nudge']}")

    # Display Trace
    with st.expander("Full Reasoning Trace"):
        st.json(result['trace'])
    st.markdown("---")

def run_streamlit_app():
    st.set_page_config(page_title="Nivra Multi-Agent Planner", layout="wide")
    st.title("🔥 Nivra: Final Multi-Agent Demo")
    st.info("Demonstrating Safety, Memory Nudging, and Multi-Channel Sensing.")

    # --- Scenario Definitions ---

    # T3/GROWTH Scenario: Stable user, low risk, high discipline, gets growth plan + relevant coach advice
    display_scenario(
        "T3/GROWTH: Stable Finances, High Discipline",
        user_id="stable_user",
        sms="Debit $15.00 purchase.",
        manual=[{"category": "FOOD", "amount": 5.00}],
        ocr_text="GROCERY $75.00"
    )

    # T1/SURVIVAL Scenario: Fragile user, high expense, low confidence -> Safety Fallback Triggered
    display_scenario(
        "T1/SURVIVAL: High Risk/Low Confidence (Safety Fallback)",
        user_id="fragile_user",
        sms="Debit $1000.00 critical expense.",
        manual=[], # Minimal input
        ocr_text="" # Minimal input sources for low confidence
    )

    # T2/VERIFIER Scenario: Demonstrates Scam Blocking and Student Earning Options
    display_scenario(
        "T2/VERIFIER: Scam Blocking (Earning Options)",
        user_id="stable_user",
        sms="No expenses today.",
        manual=[],
        ocr_text=""
    )


if __name__ == "__main__":
    st.write("Run the main_agent functions directly in the cells below.")
