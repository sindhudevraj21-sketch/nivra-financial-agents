from project.core.a2a_protocol import SenseState
from project.core.observability import log_event

def run_risk_analysis(state: SenseState) -> str:
    """Runs risk analysis based on financial status and data confidence."""

    # CRITICAL TRIGGER 1: Financial Ruin Risk (Shortfall exceeds 50% of remaining balance)
    if state.shortfall_projection_7d_cents >= (state.balance_est_cents * 0.5):
        log_event("RiskEvaluator", "Escalate", {"reason": "Projected Shortfall (T1)"})
        return "HIGH"

    # CRITICAL TRIGGER 2: Data Fragility/GIGO Risk (Must be below 0.5)
    if state.parser_confidence_score < 0.5:
        log_event("RiskEvaluator", "Escalate", {"reason": "Low Parser Confidence (T1)"})
        return "HIGH"

    if state.shortfall_projection_7d_cents > 0:
        return "MEDIUM"

    return "LOW"
