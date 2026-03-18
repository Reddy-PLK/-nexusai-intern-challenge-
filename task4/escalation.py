from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class CustomerContext:
    is_vip: bool
    billing_overdue: bool
    ticket_history: List[str]
    data_complete: bool


def should_escalate(
    context: CustomerContext,
    confidence_score: float,
    sentiment_score: float,
    intent: str
) -> Tuple[bool, str]:

    # Rule 4: service cancellation (highest priority)
    if intent == "service_cancellation":
        return True, "service_cancellation"

    # Rule 1: low confidence
    if confidence_score < 0.65:
        return True, "low_confidence"

    # Rule 2: angry customer
    if sentiment_score < -0.6:
        return True, "angry_customer"

    # Rule 3: repeated intent
    if context.ticket_history.count(intent) >= 3:
        return True, "repeat_complaint"

    # Rule 5: VIP + overdue billing
    if context.is_vip and context.billing_overdue:
        return True, "vip_billing_issue"

    # Rule 6: incomplete data + medium confidence
    if not context.data_complete and confidence_score < 0.80:
        return True, "incomplete_data"

    return False, "no_escalation"