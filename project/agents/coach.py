import json
import os
from typing import Dict, Any
from project.core.a2a_protocol import CoachAdvice, SenseState, PlannerOutput, BehaviorFingerprint

# External Libraries for Gemini
try:
    from google import genai
    from google.genai.errors import APIError
except ImportError:
    class MockClient: pass
    genai = type('module', (object,), {'Client': MockClient, 'types': type('module', (object,), {'GenerateContentConfig': lambda **kwargs: None})})
    APIError = Exception

class CoachAgent:
    def __init__(self): # Fixed: Changed _init_ to __init__
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("API Key not found.")
            self.client = genai.Client(api_key=api_key)
            self.model = 'gemini-2.5-flash'
        except Exception:
            self.client = None

    def run_concierge(self, state: SenseState, plan: PlannerOutput, memory: BehaviorFingerprint) -> CoachAdvice:

        risky_cat = memory.recent_risky_category

        # --- LLM-driven Coaching ---
        if self.client:
            prompt_data = {"Priority": plan.priority_level, "Balance": f"${state.balance_est_cents / 100:.2f}",
                           "RiskyCategory": risky_cat, "FollowStreak": memory.plan_follow_streak}

            system_prompt = (
                "You are a compassionate, expert financial concierge. Generate highly specific, 3-point advice blocks. "
                "Use detailed markdown and emojis. Tailor the optimization advice specifically to the 'RiskyCategory'. "
                "Output must be a clean JSON object."
            )
            prompt = f"Generate advice for a user with the following status: {json.dumps(prompt_data)}"

            response_schema = {"type": "object", "properties": {"investment_tip": {"type": "string"}, "optimization_suggestion": {"type": "string"}, "motivational_nudge": {"type": "string"}}, "required": ["investment_tip", "optimization_suggestion", "motivational_nudge"]}

            try:
                response = self.client.models.generate_content(
                    model=self.model, contents=[system_prompt, prompt],
                    config=genai.types.GenerateContentConfig(response_mime_type="application/json", response_schema=response_schema)
                )

                llm_data = json.loads(response.text)
                return CoachAdvice(**llm_data)

            except (APIError, json.JSONDecodeError):
                pass # Fall through to simulation

        # --- Simulation Fallback (Detailed and Personalized) ---

        # Investment Tip
        if plan.priority_level == "SURVIVAL" or state.balance_est_cents < 50000:
            tip = "## 💰 Investment Priority: Safety First\n1. *Emergency Fund:* Build a $500 safety net. \n2. *Debt Repayment:* Aggressively attack high-interest debt first."
        else:
            tip = "## 📈 Smart Investment Strategy\n1. *Automate:* Set up auto-transfer to savings. \n2. *Index Funds:* Focus on low-cost, broad-market index funds."

        # Optimization Suggestion
        opt_sugg = (
            f"## 💡 Optimization: {risky_cat} Leakage\n"
            f"1. *Analyze:* Your spending in *{risky_cat}* is high. Identify the single largest weekly expense here.\n"
            f"2. *Challenge:* Find a zero-cost alternative for one {risky_cat}-related activity this week.\n"
            f"3. *Recalculate:* Set a non-negotiable budget for this category for the next 7 days."
        )

        # Motivational Nudge
        nudge = f"Keep going! Your financial discipline is a muscle—it gets stronger with every small win. Current streak: {memory.plan_follow_streak} days."

        return CoachAdvice(investment_tip=tip, optimization_suggestion=opt_sugg, motivational_nudge=nudge)
