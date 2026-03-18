from fastapi import FastAPI
from pydantic import BaseModel
from task1.handler import handle_message
import asyncio

app = FastAPI()


# Request model
class MessageRequest(BaseModel):
    message: str
    customer_id: str
    channel: str


# API endpoint
@app.post("/message")
async def process_message(request: MessageRequest):
    result = await handle_message(
        request.message,
        request.customer_id,
        request.channel
    )
    return result