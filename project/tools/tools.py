from typing import List, Dict, Any, Tuple
from project.core.a2a_protocol import ExpenseEvent

def parse_sms_transaction(text: str) -> List[ExpenseEvent]:
    """Simulates parsing financial transactions from SMS text."""
    events = []
    if "purchase" in text.lower():
        events.append(ExpenseEvent(source="SMS", amount_cents=1500, category="FOOD"))
    if "debit $500" in text.lower():
        events.append(ExpenseEvent(source="SMS", amount_cents=50000, category="RENT"))
    return events

def parse_scanner_ocr(ocr_text: str) -> List[ExpenseEvent]:
    """Simulates parsing transactions from OCR/receipt text."""
    events = []
    if "GROCERY" in ocr_text.upper():
        events.append(ExpenseEvent(source="Scanner", amount_cents=7500, category="GROCERIES"))
    if "COFFEE" in ocr_text.upper():
        events.append(ExpenseEvent(source="Scanner", amount_cents=450, category="FOOD"))
    return events

def normalize_manual_expenses(entries: List[Dict[str, Any]]) -> List[ExpenseEvent]:
    """Normalizes manual expense entries into ExpenseEvent list."""
    normalized = []
    for entry in entries:
        try:
            amount_cents = int(float(entry.get("amount", 0)) * 100)
            category = str(entry.get("category", "MISC")).upper()
            if amount_cents > 0:
                normalized.append(ExpenseEvent(source="Manual", amount_cents=amount_cents, category=category))
        except:
            continue
    return normalized
