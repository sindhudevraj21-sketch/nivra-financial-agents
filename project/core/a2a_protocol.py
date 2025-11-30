from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class ExpenseEvent(BaseModel):
    source: str = Field(description="SMS, Manual, or Scanner")
    amount_cents: int
    category: str

class SenseState(BaseModel):
    balance_est_cents: int
    shortfall_projection_7d_cents: int
    parser_confidence_score: float = Field(description="0.0 to 1.0 confidence in all parsed data.")
    all_today_expenses: List[ExpenseEvent]

class BehaviorFingerprint(BaseModel):
    discipline_score: float = Field(description="0.0 to 1.0 plan follow rate.")
    shortfall_frequency_30d: float
    recent_risky_category: str
    plan_follow_streak: int

class PlannerRecommendation(BaseModel): # Added PlannerRecommendation
    name: str
    type: str
    risk_score: float
    relevance_tags: List[str]

class PlannerOutput(BaseModel):
    priority_level: str = Field(description="SURVIVAL, DISCIPLINE, or GROWTH")
    today_spend_limit_cents: int
    micro_task: str
    earning_suggestion: Optional[Dict[str, Any]]
    reasoning_trace: Dict[str, Any]

class CoachAdvice(BaseModel):
    investment_tip: str
    optimization_suggestion: str
    motivational_nudge: str
