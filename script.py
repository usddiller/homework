import asyncio
import websockets
import json


async def test():
    uri = "ws://127.0.0.1:8000/ws/chat/room1/"
    async with websockets.connect(uri) as ws:
        data = json.dumps({
            "user": {
                "id": 1,
                "username": "Brick_92",
                "first_name": "Anatoliy",
                "last_name": "Shevchenko"
            },
            "text": "Hello World!"
        })
        await ws.send(data)
        print(await ws.recv())

asyncio.run(test())
