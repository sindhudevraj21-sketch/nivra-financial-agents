from typing import Dict, Any, List
from project.core.a2a_protocol import BehaviorFingerprint
from collections import defaultdict
from project.core.observability import log_event

# --- FINAL: Global State for All Personas (Memory Simulation) ---
USER_SIMULATED_HISTORY = {
    "student_user": {
        "discipline_score": 0.6,
        "compliance_days": 5,
        "risky_spending": defaultdict(lambda: 0, {"DINING": 9000, "SUBSCRIPTIONS": 2000}),
    },
    "gigworker_user": {
        "discipline_score": 0.85,
        "compliance_days": 15,
        "risky_spending": defaultdict(lambda: 0, {"TRANSPORT": 7500, "MAINTENANCE": 3000}),
    },
    "salaried_user": {
        "discipline_score": 0.7,
        "compliance_days": 10,
        "risky_spending": defaultdict(lambda: 0, {"RETAIL": 12000, "TRAVEL": 5000}),
    },
    "retiree_user": { # NEW: Fixed income, low risk tolerance
        "discipline_score": 0.9,
        "compliance_days": 30,
        "risky_spending": defaultdict(lambda: 0, {"HEALTH": 15000, "INSURANCE": 10000}),
    },
    "artist_user": { # NEW: Volatile income, high creative spending
        "discipline_score": 0.55,
        "compliance_days": 2,
        "risky_spending": defaultdict(lambda: 0, {"HOBBIES": 8000, "MISC": 4000}),
    },
    "family_user": { # NEW: High fixed costs, large household
        "discipline_score": 0.65,
        "compliance_days": 7,
        "risky_spending": defaultdict(lambda: 0, {"CHILDREN": 10000, "HOUSING": 15000}),
    },
    "stable_user": {
        "discipline_score": 0.9,
        "compliance_days": 20,
        "risky_spending": defaultdict(lambda: 0, {"FOOD": 1000, "MISC": 500}),
    },
    "fragile_user": {
        "discipline_score": 0.4,
        "compliance_days": 1,
        "risky_spending": defaultdict(lambda: 0, {"RETAIL": 8000, "COFFEE": 6000}),
    }
}

def identify_riskiest_category(user_id: str) -> str:
    """Identifies the category with the highest simulated recent spending."""
    history = USER_SIMULATED_HISTORY.get(user_id, {})
    if not history or not history["risky_spending"]:
        return "MISC"

    riskiest_cat = max(history["risky_spending"], key=history["risky_spending"].get)
    return riskiest_cat


class SessionMemory:
    def __init__(self, user_id: str):
        self.user_id = user_id
        # Set a reasonable default if the ID isn't found
        if user_id not in USER_SIMULATED_HISTORY:
            USER_SIMULATED_HISTORY[user_id] = {
                "discipline_score": 0.6,
                "compliance_days": 3,
                "risky_spending": defaultdict(lambda: 0, {"FOOD": 3000}),
            }

    def compute_and_get_fingerprint(self) -> BehaviorFingerprint:
        """Calculates and returns the current state of the user's behavioral fingerprint."""

        user_data = USER_SIMULATED_HISTORY[self.user_id]

        discipline = min(0.95, max(0.1, user_data["discipline_score"]))
        risky_category = identify_riskiest_category(self.user_id)
        shortfall_freq = 0.05 if discipline < 0.5 else 0.01

        return BehaviorFingerprint(
            discipline_score=discipline,
            shortfall_frequency_30d=shortfall_freq,
            recent_risky_category=risky_category,
            plan_follow_streak=user_data["compliance_days"]
        )

    # Function to simulate compliance update
    def update_compliance(self, complied: bool, spend_limit_cents: int):
        user_data = USER_SIMULATED_HISTORY[self.user_id]

        if complied:
            user_data["compliance_days"] += 1
            user_data["discipline_score"] = min(0.95, user_data["discipline_score"] + 0.05)
        else:
            user_data["compliance_days"] = 0
            user_data["discipline_score"] = max(0.1, user_data["discipline_score"] - 0.1)

        log_event("SessionMemory", "ComplianceUpdate", {"user": self.user_id, "score": user_data["discipline_score"]})
