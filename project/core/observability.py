import json
import time
from typing import Dict, Any

def log_event(agent: str, event_type: str, data: Dict[str, Any]):
    """Logs agent events with timestamps."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "agent": agent,
        "event_type": event_type,
        "data": data
    }
    print(f"[LOG] {json.dumps(log_entry)}")

def generate_trace(context: Dict[str, Any], plan_output: Dict[str, Any], coach_advice: Dict[str, Any]) -> Dict[str, Any]:
    """Generates the final human-readable reasoning trace."""

    verification_status = context.get("verification_status", "N/A")
    verified_recs_count = len(context.get("verified_recs", []))
    detailed_verification_summary = f"Status: {verification_status}, Recommended Items: {verified_recs_count}"

    trace = {
        "priority_level": plan_output.get("priority_level"),
        "risk_report": context.get("risk_level"),
        "memory_snapshot": context.get("memory_snapshot").model_dump(), # Changed .dict() to .model_dump()
        "input_hygiene": {
            "parser_confidence": context["sense_state"]["parser_confidence_score"],
            "total_expenses_recorded": len(context["sense_state"]["all_today_expenses"])
        },
        "verification_summary": detailed_verification_summary,
        "planner_reasoning": plan_output.get("reasoning_trace"),
        "coach_summary": coach_advice
    }
    return trace
