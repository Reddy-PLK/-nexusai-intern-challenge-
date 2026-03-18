from dataclasses import dataclass
from typing import Optional
from task2.database import save_message
import asyncio


# Response structure
@dataclass
class MessageResponse:
    response_text: str
    confidence: float
    suggested_action: str
    channel_formatted_response: str
    error: Optional[str]


# Main async function
async def handle_message(customer_message: str, customer_id: str, channel: str) -> MessageResponse:

    # Error case 1: empty input
    if not customer_message.strip():
        return MessageResponse(
            response_text="",
            confidence=0.0,
            suggested_action="none",
            channel_formatted_response="",
            error="empty_input"
        )

    try:
        # Mock AI logic (no API needed)

        message = customer_message.lower()

        if "internet" in message:
            response_text = "Please restart your router and check all cables."
            confidence = 0.9
            suggested_action = "troubleshoot"

        elif "billing" in message or "payment" in message:
            response_text = "Please check your billing details in the app or contact support."
            confidence = 0.85
            suggested_action = "billing_support"

        elif "sim" in message:
            response_text = "Try reinserting your SIM card or restart your phone."
            confidence = 0.8
            suggested_action = "troubleshoot"

        elif "cancel" in message:
            response_text = "We’re sorry to hear that. Let me connect you to a human agent."
            confidence = 0.95
            suggested_action = "escalate"

        else:
            response_text = "Thank you for your message. Our support team will assist you shortly."
            confidence = 0.7
            suggested_action = "general_response"

        # Channel formatting
        if channel == "voice":
            channel_response = response_text[:100]  # short response
        else:
            channel_response = response_text
            
        save_message(customer_id, customer_message, response_text)

        return MessageResponse(
            response_text=response_text,
            confidence=confidence,
            suggested_action=suggested_action,
            channel_formatted_response=channel_response,
            error=None
        )

    except Exception as e:
        return MessageResponse(
            response_text="",
            confidence=0.0,
            suggested_action="failed",
            channel_formatted_response="",
            error=str(e)
        )