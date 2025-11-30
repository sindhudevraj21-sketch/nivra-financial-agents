from typing import Dict, Any, List
import json
from project.core.a2a_protocol import BehaviorFingerprint, PlannerRecommendation

def engineer_planner_context(sense_state: Dict[str, Any], memory_snapshot: Dict[str, Any], verified_recs: List[Dict[str, Any]], risk_level: str) -> str:
    """
    Engineers a detailed, structured, and FIXED-SIZE prompt for the LLM Planner.
    """
    context = {
        "SENSE_STATE": sense_state,
        "MEMORY_SNAPSHOT": memory_snapshot,
        "RISK_LEVEL": risk_level,
        "VERIFIED_EARNING_RECS": verified_recs, # Now expects a list of dictionaries directly
        "INSTRUCTION": "Generate a micro-plan. If RISK_LEVEL is HIGH, prioritize SURVIVAL and omit earning recs."
    }

    return json.dumps(context, indent=2)
