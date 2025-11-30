from typing import Dict, Any, List
import json
from project.core.a2a_protocol import BehaviorFingerprint, PlannerRecommendation # Import PlannerRecommendation

def engineer_planner_context(sense_state: Dict[str, Any], memory_snapshot: BehaviorFingerprint, verified_recs: List[PlannerRecommendation], risk_level: str) -> str:
    """
    Engineers a detailed, structured, and FIXED-SIZE prompt for the LLM Planner.
    """
    # Convert PlannerRecommendation objects to dictionaries for JSON serialization
    serialized_recs = [rec.model_dump() for rec in verified_recs] # Changed .dict() to .model_dump()

    context = {
        "SENSE_STATE": sense_state,
        "MEMORY_SNAPSHOT": memory_snapshot.model_dump(), # Changed .dict() to .model_dump()
        "RISK_LEVEL": risk_level,
        "VERIFIED_EARNING_RECS": serialized_recs, # Use the serialized list here
        "INSTRUCTION": "Generate a micro-plan. If RISK_LEVEL is HIGH, prioritize SURVIVAL and omit earning recs."
    }

    return json.dumps(context, indent=2)
