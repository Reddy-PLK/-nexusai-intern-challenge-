from dataclasses import dataclass
from typing import Optional
import asyncio
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


@dataclass
class MessageResponse:
    response_text: str
    confidence: float
    suggested_action: str
    channel_formatted_response: str
    error: Optional[str]


SYSTEM_PROMPT = """
You are a telecom support AI.

Help users with:
- network issues
- billing problems
- SIM issues

Rules:
- Be polite and clear
- Voice responses must be under 2 sentences
- Chat responses can be longer
- Suggest escalation if needed
"""


async def handle_message(customer_message: str, customer_id: str, channel: str) -> MessageResponse:

    # Empty input
    if not customer_message.strip():
        return MessageResponse("", 0.0, "none", "", "empty_input")

    try:
        response = await asyncio.wait_for(
            openai.ChatCompletion.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": customer_message}
                ]
            ),
            timeout=10
        )

        ai_text = response["choices"][0]["message"]["content"]

        # Channel formatting
        if channel == "voice":
            formatted = ai_text[:150]
        else:
            formatted = ai_text

        return MessageResponse(ai_text, 0.9, "resolve", formatted, None)

    except asyncio.TimeoutError:
        return MessageResponse("", 0.0, "retry", "", "timeout")

    except openai.error.RateLimitError:
        await asyncio.sleep(2)

        try:
            retry = await openai.ChatCompletion.acreate(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": customer_message}
                ]
            )

            ai_text = retry["choices"][0]["message"]["content"]

            return MessageResponse(ai_text, 0.85, "resolve", ai_text, None)

        except:
            return MessageResponse("", 0.0, "failed", "", "rate_limit_failed")