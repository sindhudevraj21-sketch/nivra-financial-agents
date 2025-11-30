import sys, os
import json
from typing import Dict, Any, List

# Add project root to path for local imports
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

# Clear cached modules to ensure latest changes are picked up
modules_to_delete = [m for m in sys.modules if m.startswith('project')]
for module_name in modules_to_delete:
    del sys.modules[module_name]

from project.main_agent import run_agent
from project.memory.session_memory import USER_SIMULATED_HISTORY, identify_riskiest_category

def execute_edge_case(
    name: str,
    user_id: str,
    sms_input: str,
    manual_entries: List[Dict[str, Any]],
    ocr_text: str,
    expected_priority: str,
    expected_micro_task_keywords: List[str],
    expected_earning_name_keywords: List[str]
):
    print(f"\n--- Running Test Case: {name} (User: {user_id}) ---")
    overall_test_pass = True
    try:
        result = run_agent(
            sms_input=sms_input,
            user_id=user_id,
            manual_entries=manual_entries,
            ocr_text=ocr_text
        )

        plan = result['plan']
        coach = result['coach_advice']
        trace = result['trace']

        # Validation for Priority Level
        priority_pass = plan['priority_level'] == expected_priority
        print(f"  Priority Level: {'PASS' if priority_pass else 'FAIL'} - Expected: {expected_priority}, Actual: {plan['priority_level']}")
        if not priority_pass:
            overall_test_pass = False

        # Validation for Micro-Task Keywords
        micro_task_text = plan['micro_task'].lower()
        micro_task_pass = all(keyword.lower() in micro_task_text for keyword in expected_micro_task_keywords)
        print(f"  Micro-Task Keywords: {'PASS' if micro_task_pass else 'FAIL'} - Expected: {expected_micro_task_keywords}, Actual: {plan['micro_task']}")
        if not micro_task_pass:
            overall_test_pass = False

        # Validation for Earning Suggestion Keywords
        earning_suggestion = plan.get('earning_suggestion')
        earning_name_pass = True
        actual_earning_name = earning_suggestion.get('name', '') if earning_suggestion else 'None'

        if expected_earning_name_keywords: # Expecting an earning suggestion
            if earning_suggestion:
                earning_name_lower = actual_earning_name.lower()
                earning_name_pass = any(keyword.lower() in earning_name_lower for keyword in expected_earning_name_keywords)
            else: # Expected an earning suggestion but got None
                earning_name_pass = False
        else: # Not expecting an earning suggestion (e.g., SURVIVAL mode)
            earning_name_pass = earning_suggestion is None

        print(f"  Earning Suggestion: {'PASS' if earning_name_pass else 'FAIL'} - Expected keywords: {expected_earning_name_keywords if expected_earning_name_keywords else 'None'}")
        print(f"    Actual Earning Suggestion: {actual_earning_name}")
        if not earning_name_pass:
            overall_test_pass = False

        print("\n  --- Summary from Agent Trace ---")
        print(f"  Risk Level: {trace['risk_report']}")
        print(f"  Parser Confidence: {trace['input_hygiene']['parser_confidence']:.2f}")
        print(f"  Coach Investment Tip (first line): {coach['investment_tip'].splitlines()[0]}")

    except Exception as e:
        print(f"  [TEST ERROR] Test case '{name}' failed with an exception: {e}")
        overall_test_pass = False
    finally:
        print(f"\n  OVERALL TEST RESULT FOR '{name}': {'PASSED' if overall_test_pass else 'FAILED'}")
        return overall_test_pass

# List to keep track of test results
all_tests_passed = []

# --- Test Cases ---

# E1: T1 Low Confidence - Fragile User (SURVIVAL)
# Triggers SURVIVAL because only 1 input source leads to parser_confidence < 0.5
all_tests_passed.append(execute_edge_case(
    name="E1: T1 Low Confidence - Fragile User",
    user_id="fragile_user",
    sms_input="Debit $10.00 purchase.",
    manual_entries=[],
    ocr_text="",
    expected_priority="SURVIVAL",
    expected_micro_task_keywords=["emergency", "halt", "discretionary"],
    expected_earning_name_keywords=[]
))

# E2: T1 High Shortfall - Stable User (SURVIVAL)
# Triggers SURVIVAL due to a large expense causing a high shortfall
all_tests_passed.append(execute_edge_case(
    name="E2: T1 High Shortfall - Stable User",
    user_id="stable_user",
    sms_input="Debit $1400.00 major payment.", # Increased amount to trigger shortfall condition
    manual_entries=[],
    ocr_text="",
    expected_priority="SURVIVAL",
    expected_micro_task_keywords=["emergency", "halt", "discretionary"],
    expected_earning_name_keywords=[]
))

# E3: T2 Verifier - Stable User, Growth Priority (GROWTH)
# Sufficient inputs for high confidence, stable user, expects GROWTH with a generic earning suggestion
all_tests_passed.append(execute_edge_case(
    name="E3: T2 Verifier - Stable User, Growth Priority",
    user_id="stable_user",
    sms_input="Debit $5.00 purchase.",
    manual_entries=[{"category": "FOOD", "amount": 5.00}],
    ocr_text="Receipt: GROCERY $75.00", # Added third input for very high confidence
    expected_priority="GROWTH",
    expected_micro_task_keywords=["automate", "savings", "research", "passive income"],
    expected_earning_name_keywords=["online survey", "data annotation", "local delivery routes"] # LLM or fallback
))

# E4: T3 Memory Nudging - Fragile User, Discipline Priority (DISCIPLINE)
# Sufficient inputs for high confidence, fragile user (low discipline), expects DISCIPLINE
# Micro-task should be tailored to their 'RETAIL' risky category
fragile_risky_cat = identify_riskiest_category("fragile_user")
all_tests_passed.append(execute_edge_case(
    name="E4: T3 Memory Nudging - Fragile User, Discipline Priority",
    user_id="fragile_user",
    sms_input="Debit $20.00 purchase.",
    manual_entries=[{"category": "COFFEE", "amount": 10.00}],
    ocr_text="RETAIL Store $50.00", # Added for high confidence and risky category
    expected_priority="DISCIPLINE",
    expected_micro_task_keywords=["discipline focus", "alternative", "low-cost", fragile_risky_cat.lower()],
    expected_earning_name_keywords=["online survey", "data annotation", "local delivery routes"] # LLM or fallback
))

# E5: Student User, Academic Earning (DISCIPLINE)
# Student user (discipline_score 0.6 < 0.7), expects DISCIPLINE, academic earning suggestion
student_risky_cat = identify_riskiest_category("student_user")
all_tests_passed.append(execute_edge_case(
    name="E5: Student User, Academic Earning",
    user_id="student_user",
    sms_input="Debit $12.00 DINING.",
    manual_entries=[{"category": "BOOKS", "amount": 25.00}],
    ocr_text="UNIVERSITY COFFEE $5.00", # Ensures high confidence
    expected_priority="DISCIPLINE",
    expected_micro_task_keywords=["discipline focus", "alternative", "low-cost", student_risky_cat.lower()],
    expected_earning_name_keywords=["campus tutoring", "research assistant"] # Persona specific
))

# E6: Retiree User, Low-Stress Earning (GROWTH)
# Retiree user (discipline_score 0.9 >= 0.7), expects GROWTH, low-stress earning suggestion
all_tests_passed.append(execute_edge_case(
    name="E6: Retiree User, Low-Stress Earning",
    user_id="retiree_user",
    sms_input="Debit $5.00 pharmacy.",
    manual_entries=[{"category": "HOBBIES", "amount": 15.00}],
    ocr_text="SENIOR CENTER EVENT $10.00", # Ensures high confidence
    expected_priority="GROWTH",
    expected_micro_task_keywords=["automate", "savings", "research", "passive income"],
    expected_earning_name_keywords=["receptionist", "companion care"] # Persona specific
))

# E7: Artist User, Creative Earning (DISCIPLINE)
# Artist user (discipline_score 0.55 < 0.7), expects DISCIPLINE, creative earning suggestion
artist_risky_cat = identify_riskiest_category("artist_user")
all_tests_passed.append(execute_edge_case(
    name="E7: Artist User, Creative Earning",
    user_id="artist_user",
    sms_input="Debit $50.00 ART SUPPLIES.",
    manual_entries=[{"category": "CAFE", "amount": 8.00}],
    ocr_text="GALLERY ENTRY $12.00", # Ensures high confidence
    expected_priority="DISCIPLINE",
    expected_micro_task_keywords=["discipline focus", "alternative", "low-cost", artist_risky_cat.lower()],
    expected_earning_name_keywords=["copywriting", "photographer"] # Persona specific
))

# E8: Family User, Household Earning (DISCIPLINE)
# Family user (discipline_score 0.65 < 0.7), expects DISCIPLINE, household-related earning suggestion
family_risky_cat = identify_riskiest_category("family_user")
all_tests_passed.append(execute_edge_case(
    name="E8: Family User, Household Earning",
    user_id="family_user",
    sms_input="Debit $150.00 GROCERIES.",
    manual_entries=[{"category": "KIDS", "amount": 40.00}],
    ocr_text="HOME DEPOT $80.00", # Ensures high confidence
    expected_priority="DISCIPLINE",
    expected_micro_task_keywords=["discipline focus", "alternative", "low-cost", family_risky_cat.lower()],
    expected_earning_name_keywords=["household", "errand runner"] # Persona specific
))

print("\n=============================================")
print(f"      FINAL TEST SUITE SUMMARY: {'ALL TESTS PASSED' if all(all_tests_passed) else 'SOME TESTS FAILED'}           ")
print("=============================================")
