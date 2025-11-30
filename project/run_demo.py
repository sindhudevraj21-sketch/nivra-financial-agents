import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from project.main_agent import run_agent

if __name__ == "__main__":
    print("--- Running Nivra Main Agent Final Scenarios ---")

    # 1. T3/GROWTH Scenario (Stable user, low risk)
    result_growth = run_agent("Debit $5.00 purchase.",
                             user_id="stable_user",
                             manual_entries=[{"category": "FOOD", "amount": 5.00}])
    print("\n[T3/GROWTH Plan - Discipline/Growth Priority]")
    print(result_growth['response_summary'])

    # 2. T1/SURVIVAL Scenario (High Risk Fallback Triggered by low confidence/high expense)
    result_survival = run_agent("Debit $900.00 high-risk purchase.",
                                user_id="fragile_user",
                                manual_entries=[])
    print("\n[T1/SURVIVAL Plan - Safety Fallback Triggered]")
    print(result_survival['response_summary'])

    # 3. T2/VERIFIER Scenario (Scam Blocking implicitly tested)
    # The planner will receive the full list but only selects the HIGH-TRUST gigs.
    result_verifier = run_agent("No major expenses.", user_id="stable_user", manual_entries=[])
    print("\n[T2 Plan - Verifier Check (Growth priority)]")
    print(result_verifier['response_summary'])
