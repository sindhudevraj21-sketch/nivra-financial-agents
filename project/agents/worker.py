import time
from typing import Dict, Any, List
from project.core.a2a_protocol import SenseState, ExpenseEvent
from project.tools.tools import parse_sms_transaction, parse_scanner_ocr, normalize_manual_expenses
from project.core.observability import log_event

# --- NEW: Vendor/Category Mapping (Data Cleansing Logic) ---
VENDOR_MAP = {
    "STARBUCKS": "COFFEE", "SBX": "COFFEE", "CAFE": "COFFEE",
    "AMZN": "RETAIL", "AMAZON": "RETAIL",
    "UBEREATS": "DINING", "DOORDASH": "DINING",
    "LYFT": "TRANSPORT", "UBER": "TRANSPORT", "BUS": "TRANSPORT",
    "GROCERY": "GROCERIES", "WALMART": "GROCERIES"
}

def clean_and_categorize(expense: ExpenseEvent) -> ExpenseEvent:
    """Normalizes the category based on known vendors."""
    source_text = expense.source.upper()
    category = expense.category.upper()

    # Try to map based on source text or category
    for vendor, cat in VENDOR_MAP.items():
        if vendor in source_text or vendor in category:
            expense.category = cat
            return expense

    # Simple cleanup
    expense.category = category if category else "MISC"
    return expense


class SenseWorker:
    def run_sense_worker(self, raw_sms_input: str, manual_entries: List[Dict[str, Any]], raw_ocr_text: str) -> SenseState:

        # 1. Parsing and Normalization
        sms_expenses = parse_sms_transaction(raw_sms_input)
        manual_expenses = normalize_manual_expenses(manual_entries)
        ocr_expenses = parse_scanner_ocr(raw_ocr_text)

        all_expenses: List[ExpenseEvent] = sms_expenses + manual_expenses + ocr_expenses

        # --- NEW: Apply Data Cleansing ---
        cleaned_expenses = [clean_and_categorize(e) for e in all_expenses]
        total_spent_cents = sum(e.amount_cents for e in cleaned_expenses)

        # 2. Confidence Scoring (T1 Logic)
        num_sources = len([s for s in [raw_sms_input, manual_entries, raw_ocr_text] if s])
        parser_confidence = 0.9 if num_sources >= 2 else 0.4

        # 3. State Calculation (Initial balance is $1500)
        balance_cents = max(0, 150000 - total_spent_cents)
        avg_daily_spend = 5000
        shortfall_projection = max(0, (avg_daily_spend * 7) - balance_cents)

        state_data = {
            "balance_est_cents": balance_cents,
            "shortfall_projection_7d_cents": shortfall_projection,
            "parser_confidence_score": parser_confidence,
            "all_today_expenses": cleaned_expenses
        }

        log_event("SenseWorker", "StateGenerated", {"balance": balance_cents, "confidence": parser_confidence})

        return SenseState(**state_data)
