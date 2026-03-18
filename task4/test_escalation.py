import pytest
from task4.escalation import should_escalate, CustomerContext


def base_context():
    return CustomerContext(
        is_vip=False,
        billing_overdue=False,
        ticket_history=[],
        data_complete=True
    )


def test_low_confidence():
    """Test escalation when confidence is below threshold (critical for AI reliability)."""
    ctx = base_context()
    result = should_escalate(ctx, 0.5, 0.0, "general")
    assert result == (True, "low_confidence")


def test_angry_customer():
    """Test escalation when customer sentiment is very negative (protects user experience)."""
    ctx = base_context()
    result = should_escalate(ctx, 0.9, -0.8, "general")
    assert result == (True, "angry_customer")


def test_repeat_complaint():
    """Test escalation when same issue repeats multiple times (prevents frustration)."""
    ctx = CustomerContext(False, False, ["billing", "billing", "billing"], True)
    result = should_escalate(ctx, 0.9, 0.0, "billing")
    assert result == (True, "repeat_complaint")


def test_service_cancellation():
    """Test that cancellation always escalates (business-critical rule)."""
    ctx = base_context()
    result = should_escalate(ctx, 0.99, 0.5, "service_cancellation")
    assert result == (True, "service_cancellation")


def test_vip_billing_issue():
    """Test escalation for VIP customers with billing problems (high priority users)."""
    ctx = CustomerContext(True, True, [], True)
    result = should_escalate(ctx, 0.9, 0.0, "billing")
    assert result == (True, "vip_billing_issue")


def test_incomplete_data():
    """Test escalation when data is incomplete and confidence is not high (risk handling)."""
    ctx = CustomerContext(False, False, [], False)
    result = should_escalate(ctx, 0.75, 0.0, "general")
    assert result == (True, "incomplete_data")


# EDGE CASE 1
def test_no_escalation():
    """Test normal scenario where no rule triggers (AI should handle)."""
    ctx = base_context()
    result = should_escalate(ctx, 0.9, 0.2, "general")
    assert result == (False, "no_escalation")


# EDGE CASE 2
def test_multiple_rules_priority():
    """Test priority: cancellation should override all other rules."""
    ctx = CustomerContext(True, True, ["service_cancellation"] * 5, False)
    result = should_escalate(ctx, 0.1, -1.0, "service_cancellation")
    assert result == (True, "service_cancellation")