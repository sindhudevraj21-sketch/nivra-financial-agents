import sys, os
from typing import Dict, Any, List
# Crucial Path Fix for imports within Colab structure
# This adds the current working directory to the path, ensuring 'project.agents' is found.
sys.path.insert(0, os.getcwd())

from project.agents.worker import SenseWorker
from project.evaluator.risk import run_risk_analysis
from project.evaluator.verifier import run_deterministic_verifier
from project.agents.planner import Planner
from project.agents.coach import CoachAgent
from project.memory.session_memory import SessionMemory
from project.core.observability import log_event, generate_trace

class MainAgent:
    def __init__(self, user_id="stable_user"):
        self.user_id = user_id
        self.worker = SenseWorker()
        self.planner = Planner()
        self.coach = CoachAgent()
        self.memory = SessionMemory(user_id)
        self.context = {}

    def handle_message(self, sms_input: str, manual_entries: List[Dict[str, Any]], ocr_text: str) -> Dict[str, Any]:
        log_event("Orchestrator", "Start", {"user": self.user_id})

        # 1. SENSE (Worker)
        sense_state = self.worker.run_sense_worker(sms_input, manual_entries, ocr_text)
        self.context["sense_state"] = sense_state.model_dump() # Changed .dict() to .model_dump()

        # 2. MEMORY
        memory_snapshot = self.memory.compute_and_get_fingerprint()
        self.context["memory_snapshot"] = memory_snapshot
        self.context["user_id"] = self.user_id # Add user_id to context

        # 3. EVALUATION (Risk)
        risk_level = run_risk_analysis(sense_state)
        self.context["risk_level"] = risk_level

        # 4. EVALUATION (Verifier)
        eval_results = run_deterministic_verifier(risk_level)
        self.context.update(eval_results)

        # 5. PLAN (Planner)
        plan_output = self.planner.run_planning(self.context)

        # 6. CONCIERGE (Coach Agent)
        coach_advice = self.coach.run_concierge(sense_state, plan_output, memory_snapshot)
        self.context["coach_advice"] = coach_advice.model_dump() # Changed .dict() to .model_dump()

        # 7. OBSERVABILITY
        final_trace = generate_trace(self.context, plan_output.model_dump(), coach_advice.model_dump()) # Changed .dict() to .model_dump()

        log_event("Orchestrator", "Finish", {"plan_priority": plan_output.priority_level})

        return {
            "user_id": self.user_id,
            "plan": plan_output.model_dump(), # Changed .dict() to .model_dump()
            "coach_advice": coach_advice.model_dump(), # Changed .dict() to .model_dump()
            "response_summary": f"Plan: {plan_output.priority_level}. Limit: ${plan_output.today_spend_limit_cents / 100:.2f}. Task: {plan_output.micro_task}",
            "trace": final_trace
        }

def run_agent(sms_input: str, user_id: str = "stable_user", manual_entries: List[Dict[str, Any]] = None, ocr_text: str = "") -> Dict[str, Any]:
    """Simplified entry point for testing."""
    if manual_entries is None:
        manual_entries = []
    # Ensure all imports used inside run_agent are available to fix the import error cascade
    from project.core.a2a_protocol import ExpenseEvent # Example of a dependency import

    agent = MainAgent(user_id=user_id)
    return agent.handle_message(sms_input, manual_entries, ocr_text)
