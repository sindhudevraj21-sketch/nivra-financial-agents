from project.core.a2a_protocol import SenseState, PlannerRecommendation
from project.core.observability import log_event
from typing import Dict, Any, List # Added missing import for Dict and Any

# --- EXPANDED MOCK GIGS FOR PERSONA RELEVANCE ---
MOCK_VERIFIED_GIGS = [
    # GIGWORKER / TRANSPORT Focus
    {"name": "Local Delivery Routes", "type": "gig", "risk_score": 0.2, "relevance_tags": ["TRANSPORT", "FLEXIBLE", "GIG"]},
    {"name": "Independent Rideshare Driver (High-Rated)", "type": "gig", "risk_score": 0.2, "relevance_tags": ["TRANSPORT", "FLEXIBLE", "GIG"]},

    # STUDENT / ACADEMIC Focus
    {"name": "Campus Tutoring (Math/Science)", "type": "academic", "risk_score": 0.1, "relevance_tags": ["STUDENT", "SKILL", "FLEXIBLE"]},
    {"name": "Research Assistant Data Entry", "type": "academic", "risk_score": 0.1, "relevance_tags": ["STUDENT", "EASY", "REMOTE"]},

    # RETIREE / LOW-STRESS / FIXED Focus
    {"name": "Retirement Community Part-Time Receptionist", "type": "fixed", "risk_score": 0.05, "relevance_tags": ["RETIREE", "FIXED", "LOW_STRESS"]},
    {"name": "Elderly Companion Care (Low-Stress)", "type": "gig", "risk_score": 0.1, "relevance_tags": ["RETIREE", "GIG", "FLEXIBLE"]},

    # ARTIST / SALARIED / REMOTE Focus
    {"name": "Online Freelance Copywriting", "type": "remote", "risk_score": 0.3, "relevance_tags": ["FLEXIBLE", "SKILL", "ARTIST"]},
    {"name": "Family Event Photographer", "type": "gig", "risk_score": 0.25, "relevance_tags": ["FAMILY", "ARTIST", "FLEXIBLE"]},
    {"name": "Virtual Assistant for Startups", "type": "remote", "risk_score": 0.2, "relevance_tags": ["SKILL", "SALARIED", "FLEXIBLE"]},

    # FAMILY / GENERAL Focus
    {"name": "Household/Errand Runner (Local)", "type": "gig", "risk_score": 0.15, "relevance_tags": ["FAMILY", "FLEXIBLE", "GIG"]},

    # General Low-Effort Gigs
    {"name": "Online Survey/Data Annotation", "type": "remote", "risk_score": 0.1, "relevance_tags": ["ANY", "EASY", "LOW_PAY"]},

    # SCAM GIG (Must be blocked by T2 logic)
    {"name": "High-Yield Investment Trading Bot", "type": "scam", "risk_score": 0.99, "relevance_tags": []},
]


def run_deterministic_verifier(risk_level: str) -> Dict[str, Any]:
    """
    T2 Verifier: Filters planner recommendations based on T1 Risk level and fixed rules.
    """

    # 1. Filter out high-risk (scam) gigs
    safe_gigs = [
        gig for gig in MOCK_VERIFIED_GIGS
        if gig["risk_score"] < 0.5
    ]

    # 2. Convert to Pydantic objects for consistency
    verified_recs = [
        PlannerRecommendation(**gig) for gig in safe_gigs
    ]

    log_event("Verifier", "VerifiedRecs", {"count": len(verified_recs)})

    return {
        "verified_recs": verified_recs,
        "verification_status": "PASS" if len(verified_recs) > 0 else "FAIL"
    }
