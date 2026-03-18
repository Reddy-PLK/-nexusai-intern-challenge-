import asyncio
from handler import handle_message


async def test():
    result = await handle_message(
        "My internet is not working",
        "cust123",
        "chat"
    )
    print(result)


asyncio.run(test())